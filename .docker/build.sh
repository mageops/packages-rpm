#!/usr/bin/env bash
set -euo pipefail

# Important! this allows us to use not globs for not existing files in for loops
shopt -s nullglob
EXTRA_MOCK_OPTS=()

# We need to do some stuff as root beofore we drop our privilyges
if [ "${UID}" = "0" ];then
    # Load rpm key for signing and drop privlidges
    if [ -n "${MGS_RPM_GPG_KEY_PUB:-}" ];then
        echo "$MGS_RPM_GPG_KEY_PUB" > ~/rpm-gpg-key.pub.asc
        rpm --import ~/rpm-gpg-key.pub.asc
    fi
    exec env HOME="/home/builder" setpriv --reuid=builder --regid=builder --init-groups "$0"
fi

import_gpg_key() {
    echo "Importing GPG key..."
    KID="$(echo "$MGS_RPM_GPG_KEY_SEC" | gpg --with-colons --import-options show-only --import | awk -F: '/^(sec|pub):/ { print $5 }')"
    echo "%_gpg_name $KID" >> ~/.rpmmacros
    echo "${MGS_RPM_GPG_KEY_SEC}" | gpg --import --batch

    # Remove passpharse to allow automatic signing
    echo -e "${MGS_RPM_GPG_KEY_PASSPHRASE}\n\n" | gpg --command-fd 0 --pinentry-mode loopback \
        --change-passphrase ${KID}
}

prepare_srpm() {
    # path to spec file
    local pkg=$1

    echo ""
    echo ""
    echo "Build SRPM fpr $pkg"

    # Cleanup
    rm -rf ~/rpmbuild/SRPMS/* ~/rpmbuild/SOURCES/*

    cp -R "$(dirname "$pkg")"/* ~/rpmbuild/SOURCES/
    spectool -g -R "$pkg"
    rpmbuild -bs "$pkg"
}

build_pkg() {
    local cfg=$1
    print_header "$cfg"
    rm -rf ~/rpmbuild/BUILD/*
    /usr/bin/mock -v -r "$cfg" --resultdir=~/rpms --rpmbuild_timeout=$((60 * 60)) ~/rpmbuild/SRPMS/*.rpm "${EXTRA_MOCK_OPTS[@]}"

    echo ""
    echo ""
}

# If we build rpm that already exists, this means that we
safe_move() {
    local src=$1
    local dest_dir=$2
    local dest

    dest="${dest_dir}/$(basename $src)"
    if [ -e "$dest" ];then
        echo "$dest already exists! Did you forgot to bump package version?"
        return 1
    fi
    mv -n "$src" "$dest"
}

export_packages() {
    local dest
    local pkg

    for arch in x86_64 aarch64;do
        # Move debuginfo packages
        for pkg in ./rpms/*-debuginfo-*."$arch".rpm;do
            safe_move "$pkg" ~/repo/"$arch"-debug/Packages
        done

        # Move debugsource packages
        for pkg in ./rpms/*-debugsource-*."$arch".rpm;do
            safe_move "$pkg" ~/repo/"$arch"-debug/Packages
        done

        # Move all other packages
        for pkg in ./rpms/*."$arch".rpm;do
            safe_move "$pkg" ~/repo/"$arch"/Packages
        done
    done

    # Move noarch packages
    for pkg in ./rpms/*.noarch.rpm;do
        safe_move "$pkg" ~/repo/noarch/Packages
    done

    # Move sources packages
    for pkg in ./rpms/*.src.rpm;do
        safe_move "$pkg" ~/repo/sources/Packages
    done
}

is_spec_unchanged() {
    local pkg=$1

    grep "  $pkg$" ~/repo/spec-cache.sum | sha256sum -c --status || return 1
}

update_repo() {
    local repo_dir=$1
    shift
    local extra_dirs=("$@")

    local dep
    local name
    for dep in "${extra_dirs[@]}";do
        name="$(basename "$dep")"
        rm -rf "${repo_dir:?}/$name"
        ln -r -s $dep "$repo_dir/$name"
    done

    echo "Updating repository $repo_dir..."
    # Deltarpm up to 64M
    createrepo --update --deltas --max-delta-rpm-size=67108864 --zck "$repo_dir"

    if [ -n "${MGS_RPM_GPG_KEY_SEC:-}" ];then
        # Sign repository
        echo "Signing..."
        rm -f "$repo_dir"/repodata/repomd.xml.asc
        gpg --detach-sign --armor "$repo_dir"/repodata/repomd.xml
        echo "$MGS_RPM_GPG_KEY_PUB" > "$repo_dir/RPM-GPG-KEY-MAGEOPS"
    fi
}

update_all_repos() {
    update_repo ~/repo/sources
    update_repo ~/repo/x86_64 ~/repo/noarch
    update_repo ~/repo/x86_64-debug
    update_repo ~/repo/aarch64 ~/repo/noarch
    update_repo ~/repo/aarch64-debug
}

print_banner() {
    echo ""
    echo ""
    echo "=========================================="
    echo " $*"
    echo "=========================================="
    echo ""
}

print_header() {
    echo ""
    echo ""
    echo "    -=- $* -=-"
}

failed_pkg() {
    local pkg=$1
    print_banner "BUILD FAILED: $pkg build failed"
    PACKAGES_FAILED+=( "$pkg" )
}


try_build_pkg() {
    local pkg=$1

    build_pkg epel-7-x86_64 || return 1
    build_pkg epel-7-aarch64 || return 1
    export_packages
    PACKAGES_LEFT=("${PACKAGES_LEFT[@]/"$pkg"}")
    PACKAGES_BUILD_IN_PASS=$(( PACKAGES_BUILD_IN_PASS + 1))
    refresh_local_repo
}

refresh_local_repo() {
    createrepo ~/repo
}

if [ -n "${MGS_RPM_GPG_KEY_SEC:-}" ];then
    import_gpg_key
else
    EXTRA_MOCK_OPTS+=( "--disable-plugin=sign" )
fi


# Initialize directories
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SPECS,SRPMS,SOURCES}
mkdir -p ~/rpms
mkdir -p ~/repo/{sources,noarch,aarch64,aarch64-debug,x86_64,x86_64-debug}/Packages

refresh_local_repo
PASS=0
PACKAGES_LEFT=(packages/*/*.spec)
while true;do
    print_banner "Starting build pass ${PASS}"
    echo "${#PACKAGES_LEFT[@]}: ${PACKAGES_LEFT[*]}"
    PACKAGES_BUILD_IN_PASS=0
    # Build updated spec files
    for pkg in "${PACKAGES_LEFT[@]}" ;do
        if is_spec_unchanged "$pkg";then
            echo "Skipping build of $pkg, as it's unchanged"
            PACKAGES_LEFT=( "${PACKAGES_LEFT[@]/"$pkg"}" )
        else
            print_banner "Building $pkg"
            prepare_srpm "$pkg"
            try_build_pkg "$pkg" || print_banner "Failed to build $pkg"
        fi
    done

    if [ "${#PACKAGES_LEFT[@]}" = 0 ];then
        print_banner "Finished building after in ${PASS} pass"
        break;
    fi

    if [ "${PACKAGES_BUILD_IN_PASS}" = 0 ] && [ "${#PACKAGES_LEFT[@]}" != 0 ];then
        print_banner "${#PACKAGES_LEFT[@]} left to build"
        for p in "${PACKAGES_LEFT[@]}";do
            echo " - $p"
        done
        exit 1
    fi

    # shellcheck disable=SC2206 # Needed to remove empty entries
    PACKAGES_LEFT=(${PACKAGES_LEFT[*]})
    PASS=$(( PASS +1 ))
    PACKAGES_BUILD_IN_PASS=0
done
rm -rf ~/repo/repodata
update_all_repos

# Update spec cache
echo "Updating spec cache..."

# shellcheck disable=SC2046 # Intetnional
sha256sum $(find packages/ -name '*.spec' -type f) > ~/repo/spec-cache.sum