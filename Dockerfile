# --- Base package build automation ---

FROM alpine:latest AS rpmbuild

RUN apk add bash make which sed curl
RUN echo -e '#!/bin/bash \n\
    \n\
    set -euo pipefail -x \n\
    \n\
    export MGS_WORKDIR="${MGS_WORKDIR:-$(pwd)}" \n\
    export MGS_MAKEFILE="${MGS_PKG_DIR:-$MGS_WORKDIR/.copr/Makefile}" \n\
    export MGS_PACKAGES_DIR="${MGS_PKG_DIR:-$MGS_WORKDIR/packages}" \n\
    export MGS_PACKAGE_DIRLIST="${@:-$(cd $MGS_PACKAGES_DIR; ls -d -- *)}" \n\
    export MGS_RPM_OUTDIR="${MGS_RPM_OUTDIR:-$MGS_WORKDIR/RPMS}" \n\
    export MGS_SRPM_OUTDIR="${MGS_SRPM_OUTDIR:-$MGS_WORKDIR/SRPMS}" \n\
    \n\
    mkdir -p "$MGS_RPM_OUTDIR" "$MGS_SRPM_OUTDIR" \n\
    echo "%_topdir $MGS_WORKDIR" >> $HOME/.rpmmacros \n\
    which dnf 2>&1 >/dev/null || (echo -e "#!/bin/bash\nif [[ \"\$1\" == \"builddep\" ]] ; then shift; yum-builddep \$@ ; else yum \$@; fi;" > /usr/bin/dnf && chmod +x /usr/bin/dnf) \n\
    \n\
    echo -e "\\n --- Running $(realpath "$0") in $MGS_WORKDIR ---\\n" \n\
    \n\
    \n\
    for _PACKAGE_DIRNAME in $MGS_PACKAGE_DIRLIST ; do \n\
        _PACKAGE_DIR="$MGS_PACKAGES_DIR/$_PACKAGE_DIRNAME/" \n\
        _PACKAGE="$(echo $_PACKAGE_DIRNAME | sed "s/^[-0-9_.]\+//")" \n\
        _SPECFILE="$_PACKAGE.spec" \n\
    \n\
        echo -e "\\n  --- Building $_PACKAGE in $_PACKAGE_DIR using $_SPECFILE ---\\n" \n\
    \n\
        make --debug --directory "$_PACKAGE_DIR" --makefile "$MGS_MAKEFILE" "spec=$_SPECFILE" "outdir=$MGS_SRPM_OUTDIR" srpm \n\
        make --debug --directory "$_PACKAGE_DIR" --makefile "$MGS_MAKEFILE" "spec=$_SPECFILE" "outdir=$MGS_RPM_OUTDIR" rpm \n\
        \n\
        echo -e "\\n  --- Package $_PACKAGE built succesfully ---\\n" \n\
    done \n\
    \n\
    echo -e "\\n  --- All packages built succesfully at $(date "+%Y-%m-%d %H:%M:%S") ---\\n"' > /usr/bin/mgs-build-rpm \
    && chmod +x /usr/bin/mgs-build-rpm \
    && rm -rf /var/cache/apk

WORKDIR /root/rpmbuild



# --- CentOS 7 ---

FROM centos:7 AS centos-7

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
    && yum -y --enablerepo=epel install elfutils-libelf rpm rpm-libs rpm-python rpm-build gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate jemalloc pcre curl sed nano which yum-utils \
    && yum -y clean all

COPY --from=rpmbuild /usr/bin/mgs-build-rpm /usr/bin/mgs-build-rpm

WORKDIR /root/rpmbuild
ENTRYPOINT [ "/usr/bin/mgs-build-rpm" ]



# --- CentOS 6 ---

FROM centos:6 AS centos-6

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm \
    && yum -y --enablerepo=epel --enablerepo=epel install elfutils-libelf rpm rpm-libs rpm-python rpm-build gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate jemalloc pcre curl sed nano which yum-utils \
    && yum -y clean all

COPY --from=rpmbuild /usr/bin/mgs-build-rpm /usr/bin/mgs-build-rpm

WORKDIR /root/rpmbuild
ENTRYPOINT [ "/usr/bin/mgs-build-rpm" ]



# --- Amazon linux 1 ---

FROM amazonlinux:1 AS amazonlinux-1

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm \
    && yum -y --enablerepo=epel install elfutils-libelf rpm rpm-libs rpm-python rpm-build gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate jemalloc pcre curl sed nano which yum-utils redhat-rpm-config \
    && yum -y clean all


COPY --from=rpmbuild /usr/bin/mgs-build-rpm /usr/bin/mgs-build-rpm

WORKDIR /root/rpmbuild
ENTRYPOINT [ "/usr/bin/mgs-build-rpm" ]



# --- Amazon linux 2 ---

FROM amazonlinux:2 AS amazonlinux-2

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && yum-config-manager --enable epel \
    && yum -y --enablerepo=epel elfutils-libelf rpm rpm-libs rpm-python rpm-build gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate jemalloc pcre curl sed nano which yum-utils redhat-rpm-config \
    && yum -y clean all

COPY --from=rpmbuild /usr/bin/mgs-build-rpm /usr/bin/mgs-build-rpm

WORKDIR /root/rpmbuild
ENTRYPOINT [ "/usr/bin/mgs-build-rpm" ]



# --- Fedora 28 ---

FROM fedora:28 AS fedora-28

RUN dnf -y install elfutils-libelf rpm rpm-libs rpm-python rpm-build gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate jemalloc pcre curl sed nano which \
    && dnf -y clean all

COPY --from=rpmbuild /usr/bin/mgs-build-rpm /usr/bin/mgs-build-rpm

WORKDIR /root/rpmbuild
ENTRYPOINT [ "/usr/bin/mgs-build-rpm" ]



# --- Fedora 31 ---

FROM fedora:31 AS fedora-31

RUN dnf -y install elfutils-libelf rpm rpm-libs rpm-python rpm-build gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate jemalloc pcre curl sed nano which \
    && dnf -y clean all

COPY --from=rpmbuild /usr/bin/mgs-build-rpm /usr/bin/mgs-build-rpm

WORKDIR /root/rpmbuild
ENTRYPOINT [ "/usr/bin/mgs-build-rpm" ]

