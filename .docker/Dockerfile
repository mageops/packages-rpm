FROM centos:7

RUN yum -y install epel-release \
    && yum-config-manager --enable epel \
    && yum -y makecache --disablerepo='*' --enablerepo=epel

RUN yum -y install \
        rpm \
        rpm-libs \
        rpm-python \
        rpm-build \
        rpm-sign \
        rpmdevtools \
        createrepo \
        elfutils-libelf \
        gcc \
        gcc-c++ \
        git \
        m4 \
        cmake \
        make \
        automake \
        autoconf \
        curl \
        sed \
        nano \
        which \
        file \
        gnupg \
        epel-rpm-macros \
        pygpgme \
        yum-utils \
        yum-builddep \
        python3-devel \
        python3-virtualenv \
    && yum -y clean all

COPY / /

RUN rpmbuild-mgs-repo-preinstall --enable \
    varnish60lts \
    nginx

ENV MGS_OS_RELEASE="el" \
    MGS_OS_RELEASEVER="7" \
    MGS_WORKDIR="/root/rpmbuild" \
    MGS_PACKAGES_DIR="/root/rpmbuild/packages" \
    MGS_RPMBUILD_ROOTDIR="/root/rpmbuild/buildtree" \
    MGS_RPMBUILD_REPODIR="/root/rpmbuild/repo" \
    MGS_RPM_GPG_KEY_SEC="/root/rpmbuild/rpm-gpg-key.sec.asc" \
    MGS_RPM_GPG_KEY_PUB="/root/rpmbuild/rpm-gpg-key.pub.asc" \
    MGS_RPM_GPG_KEY_PASSPHRASE="" \
    MGS_RPMBUILD_SIGN="no" \
    MGS_RPMBUILD_CREATE_REPO="no"

WORKDIR /root/rpmbuild
ENTRYPOINT [ "/usr/local/bin/rpmbuild-mgs" ]







