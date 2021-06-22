#!/usr/bin/env bash
set -euo pipefail

# Important! this allows us to use not globs for not existing files in for loops
shopt -s nullglob
EXTRA_MOCK_OPTS=()
FAILED_AARCH64=()

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
    /usr/bin/mock -v -r "$cfg" --resultdir=~/rpms --rpmbuild_timeout=$((15 * 60)) ~/rpmbuild/SRPMS/*.rpm "${EXTRA_MOCK_OPTS[@]}"

    echo ""
    echo ""
}

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

    echo "Updating repository $repo_dir..."
    # Deltarpm up to 64M
    createrepo --split --update --deltas --max-delta-rpm-size=67108864 --zck "$repo_dir" "${extra_dirs[@]}"

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

failed_aarch64_pkg() {
    local pkg=$1
    print_banner "BUILD FAILED: $pkg aarch64 build failed, ignoring"
    FAILED_AARCH64+=( "$pkg" )
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

# Build updated spec files
for pkg in packages/*/*.spec;do
    if is_spec_unchanged "$pkg";then
        echo "Skipping build of $pkg, as it's unchanged"
    else
        print_banner "Building $pkg"
        prepare_srpm "$pkg"

        build_pkg epel-7-x86_64
        # We currently do not support aarch64 yet, therefore do not fail build on aarch64 failure
        build_pkg epel-7-aarch64 || failed_aarch64_pkg "$pkg"
        export_packages
    fi
done

update_all_repos

# Update spec cache
echo "Updating spec cache..."
sha256sum $(find packages/ -name '*.spec' -type f) > ~/repo/spec-cache.sum


if [ ${FAILED_AARCH64[#]} -gt 0 ];then
    print_banner "Soma packages failed to build on aarch64:"
    for pkg in "${FAILED_AARCH64[@]}";do
        echo "   - $pkg"
    done
fi
