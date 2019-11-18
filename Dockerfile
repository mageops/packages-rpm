ARG CS_RPM_BUILD_WORKDIR=/root/rpmbuild
ARG CS_RPM_BUILD_ENTRYPOINT=/sbin/cs-build-rpm

# Base build automation scripts
# (the image is not important, alpine is used as it's small)

FROM alpine:latest AS build-rpm

ARG CS_RPM_BUILD_WORKDIR
ARG CS_RPM_BUILD_ENTRYPOINT

ENV CS_RPM_BUILD_ROOT=${CS_RPM_BUILD_WORKDIR} \
    CS_RPM_BUILD_SCRIPT=${CS_RPM_BUILD_ENTRYPOINT} \
    CS_RPM_PACKAGES_DIR=${CS_RPM_BUILD_WORKDIR}/packages \
    CS_RPM_COPR_MAKEFILE=${CS_RPM_BUILD_WORKDIR}/.copr/Makefile

RUN echo ${CS_RPM_BUILD_ROOT}
RUN echo '%_topdir /root/rpmbuild' > /root/.rpmmacros

RUN mkdir -p ${CS_RPM_BUILD_ROOT} ${CS_RPM_BUILD_ROOT}/RPMS ${CS_RPM_BUILD_ROOT}/SRPMS \
    && echo -e '#!'"/bin/bash\n\
    set -euo pipefail\n\
    \n\
    CS_RPM_PACKAGES=\"\${@:-\$(cd \$CS_RPM_PACKAGES_DIR; echo *)}\" \n\n\
    echo -e \"\n\n --- Starting build for packages: \$CS_RPM_PACKAGES\"\n\
    \n\
    for CS_PACKAGE in \$CS_RPM_PACKAGES ; do\n\
        CS_PACKAGE_DIR=\"\$CS_RPM_PACKAGES_DIR/\$CS_PACKAGE/\"\n\
        echo -e \"\n\n --- [\$CS_PACKAGE] [BUILD] [SRPM] --- \n\n\"\n\
        make --debug --directory \$CS_PACKAGE_DIR --makefile \$CS_RPM_COPR_MAKEFILE spec=\$CS_PACKAGE.spec outdir=\$CS_RPM_BUILD_ROOT/SRPMS srpm \n\
        echo -e \"\n\n --- [\$CS_PACKAGE] [BUILD] [SRPM] [SUCCESS] --- \n\n\"\n\
        \n\
        echo -e \"\n\n --- [\$CS_PACKAGE] [BUILD] [RPM] --- \n\n\"\n\
        make --debug --directory \$CS_PACKAGE_DIR --makefile \$CS_RPM_COPR_MAKEFILE spec=\$CS_PACKAGE.spec outdir=\$CS_RPM_BUILD_ROOT/RPMS rpm \n\
        echo -e \"\n\n --- [\$CS_PACKAGE] [BUILD] [RPM] [SUCCESS] --- \n\n\"\n\
    done\n" > ${CS_RPM_BUILD_SCRIPT} \
    && chmod +x ${CS_RPM_BUILD_SCRIPT}

# CentOS 7

FROM centos:7 AS centos-7

ARG CS_RPM_BUILD_WORKDIR
ARG CS_RPM_BUILD_ENTRYPOINT

ENV CS_RPM_BUILD_ROOT=${CS_RPM_BUILD_WORKDIR} \
    CS_RPM_BUILD_SCRIPT=${CS_RPM_BUILD_ENTRYPOINT} \
    CS_RPM_PACKAGES_DIR=${CS_RPM_BUILD_WORKDIR}/packages \
    CS_RPM_COPR_MAKEFILE=${CS_RPM_BUILD_WORKDIR}/.copr/Makefile

RUN yum -y makecache fast \
    && yum -y update \
    && gpg --import /etc/pki/rpm-gpg/* \
    && yum -y install elfutils-libelf rpm rpm-libs rpm-python rpm-build yum-utils \
    gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate nano which \
    && yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum-config-manager --enable epel && yum -y install jemalloc pcre \
    && curl -s https://packagecloud.io/install/repositories/varnishcache/varnish60lts/script.rpm.sh | bash \
    && yum -y --disablerepo=epel install varnish varnish-devel \
    && yum -y clean all \
    && ln -s `which yum` /usr/bin/dnf

COPY --from=build-rpm /root/ /root/

WORKDIR ${CS_RPM_BUILD_WORKDIR}
ENTRYPOINT ["/sbin/cs-build-rpm"]

# CentOS 6

FROM centos:6 AS centos-6

ARG CS_RPM_BUILD_WORKDIR
ARG CS_RPM_BUILD_ENTRYPOINT

ENV CS_RPM_BUILD_ROOT=${CS_RPM_BUILD_WORKDIR} \
    CS_RPM_BUILD_SCRIPT=${CS_RPM_BUILD_ENTRYPOINT} \
    CS_RPM_PACKAGES_DIR=${CS_RPM_BUILD_WORKDIR}/packages \
    CS_RPM_COPR_MAKEFILE=${CS_RPM_BUILD_WORKDIR}/.copr/Makefile

RUN yum -y makecache fast \
    && yum -y update \
    && gpg --import /etc/pki/rpm-gpg/* \
    && yum -y install elfutils-libelf rpm rpm-libs rpm-python rpm-build yum-utils \
    gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate nano which \
    && yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm && \
    yum-config-manager --enable epel && yum -y install jemalloc pcre \
    && curl -s https://packagecloud.io/install/repositories/varnishcache/varnish60lts/script.rpm.sh | bash \
    && yum -y --disablerepo=epel install varnish varnish-devel \
    && yum -y clean all \
    && ln -s `which yum` /usr/bin/dnf

WORKDIR ${CS_RPM_BUILD_WORKDIR}
ENTRYPOINT ["/sbin/cs-build-rpm"]

## Amazon linux 1

FROM amazonlinux:1 AS amazonlinux-1

ARG CS_RPM_BUILD_WORKDIR
ARG CS_RPM_BUILD_ENTRYPOINT

ENV CS_RPM_BUILD_ROOT=${CS_RPM_BUILD_WORKDIR} \
    CS_RPM_BUILD_SCRIPT=${CS_RPM_BUILD_ENTRYPOINT} \
    CS_RPM_PACKAGES_DIR=${CS_RPM_BUILD_WORKDIR}/packages \
    CS_RPM_COPR_MAKEFILE=${CS_RPM_BUILD_WORKDIR}/.copr/Makefile

RUN yum -y makecache fast \
    && yum -y update \
    && gpg --import /etc/pki/rpm-gpg/* \
    && yum -y install elfutils-libelf rpm rpm-libs rpm-python rpm-build yum-utils \
    gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate nano which \
    && yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm && \
    yum-config-manager --enable epel && yum -y install jemalloc pcre \
    && yum -y install redhat-rpm-config \
    && curl -s https://packagecloud.io/install/repositories/varnishcache/varnish60lts/script.rpm.sh | bash \
    && yum -y --disablerepo=amzn-updates,amzn-main,epel install varnish varnish-devel \
    && yum -y clean all \
    && ln -s `which yum` /usr/bin/dnf

COPY --from=build-rpm /root/ /root/

WORKDIR ${CS_RPM_BUILD_WORKDIR}
ENTRYPOINT ["/sbin/cs-build-rpm"]

## Amazon linux 2

FROM amazonlinux:2 AS amazonlinux-2

ARG CS_RPM_BUILD_WORKDIR
ARG CS_RPM_BUILD_ENTRYPOINT

ENV CS_RPM_BUILD_ROOT=${CS_RPM_BUILD_WORKDIR} \
    CS_RPM_BUILD_SCRIPT=${CS_RPM_BUILD_ENTRYPOINT} \
    CS_RPM_PACKAGES_DIR=${CS_RPM_BUILD_WORKDIR}/packages \
    CS_RPM_COPR_MAKEFILE=${CS_RPM_BUILD_WORKDIR}/.copr/Makefile

RUN yum -y makecache fast \
    && yum -y update \
    && gpg --import /etc/pki/rpm-gpg/* \
    && yum -y install elfutils-libelf rpm rpm-libs rpm-python rpm-build yum-utils \
    gcc-c++ git make autoconf automake m4 rpmdevtools gcc logrotate nano which \
    && install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum-config-manager --enable epel && yum -y install jemalloc pcre \
    && yum -y install redhat-rpm-config \
    && curl -s https://packagecloud.io/install/repositories/varnishcache/varnish60lts/script.rpm.sh | bash \
    && yum -y --disablerepo=amzn-updates,amzn-main,epel install varnish varnish-devel \
    && yum -y clean all \
    && ln -s `which yum` /usr/bin/dnf

COPY --from=build-rpm /root/ /root/

WORKDIR ${CS_RPM_BUILD_WORKDIR}
ENTRYPOINT ["/sbin/cs-build-rpm"]