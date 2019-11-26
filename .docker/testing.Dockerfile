FROM centos:7

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
    && rpm -Uvh https://mageops.github.io/rpm/repo/el/7/mageops-release.noarch.rpm

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

RUN echo " --- Install packages" >&2 \
    && yum -y install \
    varnish-modules-extra \
    varnish-module-accept \
    rabbitmq-server \
    nodejs \
    nginx \
    php \
    awscli \
    amazon-efs-utils \
    MariaDB-server