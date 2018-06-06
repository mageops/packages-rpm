#!/usr/bin/env bash

set -e

LIBMODSECVER="3.0.2"
YAJLVER="2.1.0"

BUILDIMAGE="docker.creativestyle.pl:5050/m2c/cs-rpm-build"

S3_BUCKET="cs-creativeshop-rpms"
AWS_PROFILE="creativeshop_rpms"

function build-yajl() {
    DIST="$1"
    rm -rf DEPS 
    echo "Buildiing yajl for $DIST"
    docker pull ${BUILDIMAGE}:${DIST}
    docker run --rm -v "$PWD":/root/rpmbuild ${BUILDIMAGE}:${DIST} SPEC/yajl.spec
    docker run --entrypoint '/bin/chown' --rm -v "$PWD":/root/rpmbuild ${BUILDIMAGE}:${DIST} $(id -u):$(id -g) -R .
}

function build-libmodsecurity() {
    DIST="$1"
    YAJL="$2"

    echo "Buildiing libmodsecurity for $DIST using yajl $YAJL"

    rm -rf DEPS && mkdir -p DEPS
    cp RPMS/x86_64/yajl-${YAJL}.x86_64.rpm DEPS/yajl.rpm
    cp RPMS/x86_64/yajl-devel-${YAJL}.x86_64.rpm DEPS/yajl-devel.rpm
    docker pull ${BUILDIMAGE}:${DIST}
    docker run --rm -v "$PWD":/root/rpmbuild ${BUILDIMAGE}:${DIST} SPEC/libmodsecurity.spec
    docker run --entrypoint '/bin/chown' --rm -v "$PWD":/root/rpmbuild ${BUILDIMAGE}:${DIST} $(id -u):$(id -g) -R .
    rm -rf DEPS
}

function build-nginx-creativeshop() {
    DIST="$1"
    LIBMODSECURITY="$2"
    YAJL="$3"
    echo "Buildiing nginx-creativeshop for $DIST using libmodsecurity $LIBMODSECURITY"

    rm -rf DEPS && mkdir -p DEPS
    cp RPMS/x86_64/yajl-${YAJL}.x86_64.rpm DEPS/yajl.rpm
    cp RPMS/x86_64/yajl-devel-${YAJL}.x86_64.rpm DEPS/yajl-devel.rpm
    cp RPMS/x86_64/libmodsecurity-${LIBMODSECURITY}.x86_64.rpm DEPS/libmodsecurity.rpm
    cp RPMS/x86_64/libmodsecurity-devel-${LIBMODSECURITY}.x86_64.rpm DEPS/libmodsecurity-devel.rpm
    docker pull ${BUILDIMAGE}:${DIST}
    docker run --rm -v "$PWD":/root/rpmbuild ${BUILDIMAGE}:${DIST} SPEC/nginx-creativeshop.spec
    docker run --entrypoint '/bin/chown' --rm -v "$PWD":/root/rpmbuild ${BUILDIMAGE}:${DIST} $(id -u):$(id -g) -R .
    rm -rf DEPS

}

build-yajl "amilinux-1"
build-yajl "centos-7"

build-libmodsecurity "amilinux-1" "${YAJLVER}-1.amzn1"
build-libmodsecurity "centos-7" "${YAJLVER}-1.el7"

build-nginx-creativeshop "amilinux-1" "${LIBMODSECVER}-1.amzn1" "${YAJLVER}-1.amzn1"
build-nginx-creativeshop "centos-7" "${LIBMODSECVER}-1.el7" "${YAJLVER}-1.el7"


if [ "$1" == "--upload" ] ; then
    echo '<html style="background:#fff;color:#212121;font-size:18px;"><style>a { color: #344DCC; } * { font-family: sans-serif !important; }</style><h1 style="text-align: center;"><img src="https://dev.creativeshop.io/static/frontend/Creativestyle/theme-creativeshop/en_US/images/creativeshop-logo.png" alt="creativeshop" style="width:15rem;"><br/>RPMS</h1><ul style="margin: 0 auto; max-width: 35rem;">' > 'index.html'

    export AWS_PROFILE
    find RPMS -iname '*.rpm' | sort | while read RPM ; do
        aws s3 cp --acl public-read  "${RPM}" s3://${S3_BUCKET}/
        echo "<li><a href="/$(basename $RPM)">$(basename $RPM)</a></li>" >> 'index.html'
    done

    echo '</ul></html>' >> 'index.html'
    aws s3 cp --acl public-read index.html s3://${S3_BUCKET}/index.html
    rm index.html
fi