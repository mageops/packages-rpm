#!/usr/bin/env bash

set -e -x

PUSH=$1

function build-image() {
    NAME="$1"
    LNAME="cs-rpm-build-${NAME}"
    UNAME="docker.creativestyle.pl:5050/m2c/cs-rpm-build:${NAME}"

    echo "Building image $NAME..."

    docker build -f "Dockerfile.${NAME}" -t "${LNAME}"  .

    echo "Built image ${LNAME}"

    if [ "$PUSH" == "--push" ] ; then
        docker tag "${LNAME}" "${UNAME}"
        docker push "${UNAME}"

        echo "Pushed image ${LNAME} to ${UNAME}"
    fi

    rm -rf tmp/
}

build-image "amilinux-1"
build-image "amilinux-2"
build-image "centos-6"
build-image "centos-7"
