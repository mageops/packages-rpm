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
        epel-release

RUN echo " --- Install mageops release directly from remote RPM URL" >&2 \
    && rpm -Uvh https://mageops.github.io/rpm/repo/el/7/mageops-release.noarch.rpm \
    && rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS \
    && yum -t makecache --disablerepo="*" --enablerepo="mageops"

RUN echo " --- Install mariadb-release" >&2 \
    && yum -y install mariadb-release

RUN echo " --- Install nginx-release" >&2 \
    && yum -y install nginx-release

RUN echo " --- Install nodejs-release" >&2 \
    && yum -y install nodejs-release

RUN echo " --- Install rabbitmq-release" >&2 \
    && yum -y install rabbitmq-release

RUN echo " --- Install remi-release" >&2 \
    && yum -y install remi-release

RUN echo " --- Install varnish-release" >&2 \
    && yum -y install varnish-release

RUN echo " --- Import GPG keys and make repo cache" >&2 \
    && rpm --import /etc/pki/rpm-gpg/* \
    && yum -y makecache

RUN echo " --- Install packages" >&2 \
    && yum -y install $MGS_BUILD_PKGS