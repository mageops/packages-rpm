FROM centos:7

RUN yum -y install epel-release \
    && yum-config-manager --enable epel \
    && yum -y makecache --disablerepo='*' --enablerepo=epel

RUN yum -y install \
        rpm \
        rpm-libs \
        rpm-python \
        rpm-build \
        rpmdevtools \
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
        epel-rpm-macros \
        pygpgme \
        yum-utils \
        yum-builddep \
    && yum -y clean all

COPY / /

RUN rpmbuild-mgs-repo-preinstall --enable \
    varnish60lts

WORKDIR /root/rpmbuild
ENTRYPOINT [ "/usr/local/bin/rpmbuild-mgs" ]







