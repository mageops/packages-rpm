---
layout: default
title: Build Packages
permalink: /development/build/packages
parent: Development
nav_order: 1
---

# Building the packages and repository

## Transparency

The packages are built automatically on [Travis](https://travis-ci.com/mageops/rpm).

The repository is hosted at [GitHub Pages](https://github.com/mageops/rpm/tree/gh-pages/repo/).

You can also find the build artifacts in [GitHub Releases](https://github.com/mageops/rpm/releases).

## Build locally using docker

In case you want to build the packages locally (e.g. for testing updates / modifications) you can use [Docker](https://docs.docker.com/install/).

## Build the container image locally (optional)

_You can skip this step - the image is also present at [MageOps Docker Hub Repo](https://hub.docker.com/r/mageops/rpm-build)._

```bash
docker build .docker --file .docker/Dockerfile --tag mageops/rpm-build:centos-7
```

## Run the docker image

The entrypoint script will automatically handle building the packages residing in the defined `packages/` subdirectories.

**Note! Some packages may need to be built in specific order.**

```bash
docker run --tty --volume $(pwd):/root/rpmbuild mageops/rpm-build:centos-7 {package-a-subdirectory} {package-b-subdirectory}  [...]
```

_Tip: If the above command is ran with no arguments it will build default set of packages._

**You can override the entrypoint by using the following command to get a shell to poke around in case of failure.**

```bash
docker run --interactive --tty --entrypoint /bin/bash -v $(pwd):/root/rpmbuild mageops/rpm-build:centos-7
```