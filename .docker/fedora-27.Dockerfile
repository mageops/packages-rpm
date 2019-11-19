FROM fedora:27 AS fedora-27

RUN dnf -y install \
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
        pygpgme \
        dnf-plugins-core \
    && dnf -y clean all

COPY / /

RUN rpmbuild-mgs-repo-preinstall --enable \
    varnish60lts

WORKDIR /root/rpmbuild
ENTRYPOINT [ "/usr/local/bin/rpmbuild-mgs" ]


