#!/usr/bin/env bash

# !!! This is a custom COPR-specific build environment preparation script (see: `.copr/Makefile`)

set -euo pipefail

MGS_VARNISH_REPO_NAME="${MGS_VARNISH_REPO_NAME:-varnish60lts}"

echo " --- Install official varnish 6.0 LTS repository ---"
curl -s "https://packagecloud.io/install/repositories/varnishcache/$MGS_VARNISH_REPO_NAME/script.rpm.sh" | bash
