#!/usr/bin/env bash

LIBMODSECVER="3.0.2"
S3_BUCKET="cs-creativeshop-rpms"
AWS_PROFILE="creativeshop_dev"

function build-libmodsecurity() {
    DIST="$1"
    echo "Buildiing libmodsecurity for $DIST"
    docker run --rm -v "$PWD":/root/rpmbuild docker.creativestyle.pl:5050/m2c/cs-rpm-build:${DIST} SPEC/libmodsecurity.spec
}

function build-nginx-creativeshop() {
    DIST="$1"
    LIBMODSECURITY="$2"
    echo "Buildiing nginx-creativeshop for $DIST using libmodsecurity $LIBMODSECURITY"

    cp ../libmodsecurity/RPMS/x86_64/libmodsecurity-${LIBMODSECURITY}.x86_64.rpm SOURCES/libmodsecurity.rpm
    cp ../libmodsecurity/RPMS/x86_64/libmodsecurity-devel-${LIBMODSECURITY}.x86_64.rpm SOURCES/libmodsecurity-devel.rpm
    docker pull docker.creativestyle.pl:5050/m2c/cs-rpm-build:${DIST}
    docker run --rm -v "$PWD":/root/rpmbuild docker.creativestyle.pl:5050/m2c/cs-rpm-build:${DIST} SPEC/nginx-creativeshop.spec
}

#cd libmodsecurity
#build-libmodsecurity "amilinux-1"
#build-libmodsecurity "centos-7"

cd nginx
build-nginx-creativeshop "amilinux-1" "${LIBMODSECVER}-1.amzn1"
#build-nginx-creativeshop "centos-7" "${LIBMODSECVER}-1.el7"


if [ "$1" == "--upload" ] ; then
    export AWS_PROFILE
    find {libmodsecurity,nginx}/RPMS -iname '*.rpm' | while read RPM ; do
        aws s3 cp "${RPM}" s3://${S3_BUCKET}/
    done
fi