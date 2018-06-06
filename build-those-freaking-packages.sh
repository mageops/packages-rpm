#!/usr/bin/env bash

LIBMODSECVER="3.0.2"
YAJLVER="2.1.0"

S3_BUCKET="cs-creativeshop-rpms"
AWS_PROFILE="creativeshop_rpms"

function build-yajl() {
    DIST="$1"
    echo "Buildiing yajl for $DIST"
    docker pull docker.creativestyle.pl:5050/m2c/cs-rpm-build:${DIST}
    docker run --rm -v "$PWD":/root/rpmbuild docker.creativestyle.pl:5050/m2c/cs-rpm-build:${DIST} SPEC/yajl.spec
}

function build-libmodsecurity() {
    DIST="$1"
    YAJL="$2"
    echo "Buildiing libmodsecurity for $DIST"

    mkdir -p DEPS
    ls -al DEPS
    cp RPMS/x86_64/yajl-${YAJL}.x86_64.rpm DEPS/yajl.rpm
    cp RPMS/x86_64/yajl-devel-${YAJL}.x86_64.rpm DEPS/yajl-devel.rpm
    docker pull docker.creativestyle.pl:5050/m2c/cs-rpm-build:${DIST}
    docker run --rm -v "$PWD":/root/rpmbuild docker.creativestyle.pl:5050/m2c/cs-rpm-build:${DIST} SPEC/libmodsecurity.spec
}

function build-nginx-creativeshop() {
    DIST="$1"
    LIBMODSECURITY="$2"
    YAJL="$3"
    echo "Buildiing nginx-creativeshop for $DIST using libmodsecurity $LIBMODSECURITY"

    mkdir -p DEPS
    ls -al DEPS
    cp RPMS/x86_64/yajl-${YAJL}.x86_64.rpm DEPS/yajl.rpm
    cp RPMS/x86_64/yajl-devel-${YAJL}.x86_64.rpm DEPS/yajl-devel.rpm
    cp RPMS/x86_64/libmodsecurity-${LIBMODSECURITY}.x86_64.rpm DEPS/libmodsecurity.rpm
    cp RPMS/x86_64/libmodsecurity-devel-${LIBMODSECURITY}.x86_64.rpm DEPS/libmodsecurity-devel.rpm
    docker pull docker.creativestyle.pl:5050/m2c/cs-rpm-build:${DIST}
    docker run --rm -v "$PWD":/root/rpmbuild docker.creativestyle.pl:5050/m2c/cs-rpm-build:${DIST} SPEC/nginx-creativeshop.spec

}

#build-yajl "amilinux-1"
#build-yajl "centos-7"

build-libmodsecurity "amilinux-1" "${YAJLVER}-1.amzn1"
#build-libmodsecurity "centos-7" "${YAJLVER}-1.el7"

build-nginx-creativeshop "amilinux-1" "${LIBMODSECVER}-1.amzn1" "${YAJLVER}-1.amzn1"
#build-nginx-creativeshop "centos-7" "${LIBMODSECVER}-1.el7" "${YAJLVER}-1.el7"


if [ "$1" == "--upload" ] ; then
    export AWS_PROFILE
    find RPMS -iname '*.rpm' | while read RPM ; do
        aws s3 cp "${RPM}" s3://${S3_BUCKET}/
    done
fi