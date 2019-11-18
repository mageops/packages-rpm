#!/usr/bin/env bash

set -e

SPECFILE="$1"

echo -e "\n --> Fixing perms...\n"

chown root:root -R .

echo -e "\n --> Building SPECFILE ${SPECFILE}...\n"

if [ -d "KEYS" ] ; then
    echo -e "\n --> Importing GPG keys...\n"
    find "KEYS" -iname '*.key' -exec gpg --import {} \;
fi

echo -e "\n --> Downloading sources...\n"
spectool -g -R "$SPECFILE" -C ./SOURCES

echo -e "\n --> Verifying signatures...\n"
find . -iname '*.asc' | while read SIG ; do
    set -e
    gpg --verify "$SIG"
done


if [ -d "DEPS" ] ; then
    echo -e "\n --> Install manual build dependencies...\n"
    find DEPS -iname '*.rpm' | xargs yum -y install
fi

echo -e "\n --> Installing build depenencies...\n"
yum-builddep "$SPECFILE" -y


echo -e "\n --> Building package...\n"
rpmbuild -ba "$SPECFILE"
