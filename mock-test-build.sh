#!/usr/bin/env bash

set -euo pipefail

DIR="$(dirname "${BASH_SOURCE[0]}")"

export MGS_RPM_GPG_KEY_PUB="$(cat rpm-gpg-key.pub.asc)"
export MGS_RPM_GPG_KEY_SEC="$(cat rpm-gpg-key.sec.asc)"
export MGS_RPM_GPG_KEY_PASSPHRASE=ansiblerulez

#if [ -z "$(docker images -q mockbuild)" ];then
docker build -t mockbuild:latest "$DIR/.docker"
#fi

rm -rf /tmp/packages
cp -R packages /tmp/packages

NAME=$(docker create --privileged \
    --dns 1.1.1.1 \
    -v /tmp/repo:/home/builder/repo:z \
    --rm  \
    --env MGS_RPM_GPG_KEY_PASSPHRASE="${MGS_RPM_GPG_KEY_PASSPHRASE}" \
    --env MGS_RPM_GPG_KEY_PUB="${MGS_RPM_GPG_KEY_PUB}" \
    --env MGS_RPM_GPG_KEY_SEC="${MGS_RPM_GPG_KEY_SEC}" \
    mockbuild build-rpm
)

docker cp ./packages $NAME:/home/builder/packages
docker start -ai $NAME
