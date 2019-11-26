<p align="center">
  <img align="center" alt="MageSuite" width="211" src="https://avatars2.githubusercontent.com/u/56443641?s=350&v=4">
</p>

<h1 align="center">RPM Packages</h1>

This repository contains **MageOps** RPM package collection sources and any build automation.

These are the packages that are used in [MageOps.sh](https://github.com/mageops) [ansible provisioning](https://github.com/mageops/ansible-workflow).

This means that they are mostly meant for this specific [MageSuite.io](https://github.com/magesuite) 
hosting needs, however, they are not in any way tied to our specific use-cases so they can be 
freely reused in any environment.

## Install packages from MageOps repository

### Manually 

```
rpm -Uvh https://mageops.github.io/rpm/repo/el/7/x86_64/mageops-release-7-1.noarch.rpm
```

## Distribution Support

Currently the packages are tested and working in CentOS 7 with EPEL.


## Future plans

We'll be probably packaging more software in the near time also including our internal tools.

At some point we'd also like to package *PHP* ourselves. As this is very complicated task for now
we're relying on the battle-tested [Remi's RPM repository](https://rpms.remirepo.net/).


## Package build 

### Transparency

The packages are built automatically on [Travis](https://travis-ci.com/mageops/rpm).

The repository is hosted at [GitHub Pages](https://mageops.github.io/rpm/).

You can also find the build artifact in [GitHub Releases](https://github.com/mageops/rpm/releases).

### Build locally using docker

In case you want to build the packages locally (e.g. for testing updates / modifications) you
can use [Docker](https://docs.docker.com/install/).

#### (Optional step) Build the container image locally

_You can skip this step - the image is also present at [MageOps Docker Hub Repo](https://hub.docker.com/r/mageops/rpm-build)._

```
docker build .docker --file .docker/Dockerfile --tag mageops/rpm-build:centos-7
```

#### Run the docker image

The entrypoint script will automatically handle building the packages residing in the defined `packages/` subdirectories.

**Note! Some packages may need to be built in specific order.**

```
docker run --tty --volume $(pwd):/root/rpmbuild mageops/rpm-build:centos-7 {package-a-subdirectory} {package-b-subdirectory}  [...]
```

_Tip: If the above command is ran with no arguments it will build default set of packages._

**You can override the entrypoint by using the following command to get a shell to poke around in case of failure.**

```
docker run --interactive --tty --entrypoint /bin/bash -v $(pwd):/root/rpmbuild mageops/rpm-build:centos-7
```


## Notes

```
docker build .docker --file .docker/Dockerfile --tag mageops/rpm-build:centos-7 && docker run --tty --volume $(pwd):/root/rpmbuild mageops/rpm-build:centos-7 --sign --create-repo && docker push mageops/rpm-build:centos-7
```