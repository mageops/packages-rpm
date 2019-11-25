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

### Enable using COPR plugin for yum

```
yum -y install yum-plugin-copr 
yum -y copr enable pinkeen/MageOps
```

### Enable using COPR plugin for dnf

Install dnf if you don't have it yet:

```
yum -y install epel-release
yum -y install --enablerepo=epel dnf
```

And then use dnf to enable this repository:

```
dnf -y install dnf-plugins-core
dnf -y copr enable pinkeen/MageOps
```
### Manually 

Place [this contents](https://copr.fedorainfracloud.org/coprs/pinkeen/MageOps/repo/epel-7/pinkeen-MageOps-epel-7.repo) 
into `/etc/yum.repos.d/mageops.repo` file and then generate the cache:

```
curl -s https://copr.fedorainfracloud.org/coprs/pinkeen/MageOps/repo/epel-7/pinkeen-MageOps-epel-7.repo > /etc/yum.repos.d/mageops.repo
yum -q makecache -y '--disablerepo=*' "--enablerepo=copr:copr.fedorainfracloud.org:pinkeen:MageOps"
```

https://copr-be.cloud.fedoraproject.org/results/pinkeen/MageOps/
## Distribution Support

Currently the packages are tested and working in CentOS 7 with EPEL.


## Future plans

We'll be probably packaging more software in the near time also including our internal tools.

At some point we'd also like to package *PHP* ourselves. As this is very complicated task for now
we're relying on the battle-tested [Remi's RPM repository](https://rpms.remirepo.net/).


## (Advanced) Building the packages

The packages are built automatically on [Fedora COPR](https://copr.fedorainfracloud.org/).

This is also [where the RPM repository is hosted](https://copr.fedorainfracloud.org/coprs/pinkeen/MageOps/).

### Build locally using docker

In case you want to build the packages locally (e.g. for testing updates / modifications) you
can use [Docker](https://docs.docker.com/install/).

#### (Optional step) Build the container image locally

_You can skip this step - the image is also present at [MageOps Docker Hub Repo](https://hub.docker.com/r/mageops/rpm-build)._

```
 docker build .docker --file .docker/centos-7.Dockerfile --tag mageops/rpm-build:centos-7
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
