FROM centos:7

ARG MGS_BUILD_PKGS="mageops-release"
ENV MGS_BUILD_PKGS="$MGS_BUILD_PKGS"

RUN yum -y update \
    && yum -y install \
        rpm \
        curl \
        sed \
        nano \
        which \
        file \
        gnupg \
        yum-utils \
        epel-release \
    && rpm -Uvh https://mageops.github.io/packages-rpm/repo/el/7/mageops-release.noarch.rpm \
    && rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS \
    && yum -t makecache --disablerepo="*" --enablerepo="mageops" \
    && yum -y install \
        mariadb-release \
        nginx-release \
        nodejs-release \
        rabbitmq-release \
        remi-release \
        varnish-release \
    && rpm --import /etc/pki/rpm-gpg/* \
    && yum -y makecache

RUN yum -y install $MGS_BUILD_PKGS