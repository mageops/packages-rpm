[![Build Status](https://img.shields.io/travis/mageops/rpm.svg?label=Package+Build)](https://travis-ci.com/mageops/rpm.svg?branch=master) [![Docker Hub Build Status](https://img.shields.io/docker/build/mageops/rpm-build?label=Docker+Image+Build)](https://hub.docker.com/r/mageops/rpm-build/builds)

<p align="center">
  <img align="center" alt="MageSuite" width="211" src="https://avatars2.githubusercontent.com/u/56443641?s=350&v=4">
</p>

<h1 align="center">RPM Packages</h1>

This repository contains **MageOps** RPM package collection sources and any build automation.

These are the packages that are used in [MageOps.sh](https://github.com/mageops) [ansible provisioning](https://github.com/mageops/ansible-workflow).

This means that they are mostly meant for this specific [MageSuite.io](https://github.com/magesuite) 
hosting needs, however, they are not in any way tied to our specific use-cases so they can be 
freely reused in any environment.

<p align="center">

**Get started by visiting the [Documentation](https://mageops.github.io/rpm) site!**

</p>


## TODO

- Separate travis build stages for docker, packages, repository and jekyll site
- Build dockerfile in travis?
- Also push docker image to GitHub docker repo?
- Add other packages...

## Notes

**I know I have commited secret GPG key, will generate new pair and rebuild from scratch :P**

```
docker build .docker --file .docker/Dockerfile --tag mageops/rpm-build:centos-7 && docker run --tty --volume $(pwd):/root/rpmbuild mageops/rpm-build:centos-7 --sign --create-repo && docker push mageops/rpm-build:centos-7
```

```
gpg --gen-key
gpg --export -a 'MageOps Package Manager' > rpm-gpg-key.pub.asc
gpg --export-secret-keys -a 'MageOps Package Manager' > rpm-gpg-key.sec.asc
```

```
travis login --pro
travis encrypt-file --com rpm-gpg-key.sec.asc
```