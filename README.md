<p align="center">
  <img alt="MageSuite" width="211" src="https://avatars2.githubusercontent.com/u/56443641?s=350&v=4">
  <h1>RPM Packages</h1>
</p>

This repository contains **MageOps** RPM package collection sources and any build automation.

These are the packages that are used in [MageOps.sh](https://github.com/mageops) provisioning.

This means that they are mostly meant for this specific [MageSuite.io](https://github.com/magesuite) 
hosting needs, however, they are not in any way tied to our specific use-cases so they can be 
freely reused in any environment.


## Distribution Support

Currently the packages are tested and working in CentOS 7 with EPEL.


## Package naming / conflicts

To avoid confusion the package names are suffixed with `-mageops`.

They are still marked as providers of the appropriate original software and marked
as conflicting with any common packages providing it too. This means that you won't 
be automatically upgraded to our versions upon installing the repo. This also ensures 
that you have to explicitly install our packages.


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

_You can skip this step - the image is also present on [Docker Hub](https://hub.docker.com)._

```
docker build . --tag cs-rpm-build:centos-7
```

#### Run the docker image

The entrypoint will automatically handle building the defined packages.

**Note! Some packages may need to be built in specific order.**

```
docker run --volume $(pwd):/root/rpmbuild cs-rpm-build:centos-7 {package1_to_build} {package2_to_build} [...]
```

_Tip: If the above command is ran with no arguments it will build default set of packages._

_Tip: It's recommened that you don't use the `--rm` switch to avoid having to recompile every
package every time._

**You can override the entrypoint by using the following command to get a shell to poke around in case of failure.**

```
docker run --interactive --tty --entrypoint /bin/bash -v $(pwd):/root/rpmbuild cs-rpm-build:centos-7
```

## Package notes

### libmodsecurity

Libmodsecurity is compiled without LUA support as the RHEL version is tooold. No planned support for now.

Includes support for:
  - ssdeep
  - libxml2
  - GeoIP

### nginx

Modules are dynamically linked. You need to load the module manually in your `nginx.conf`, e.g.:

```
load_module modules/ngx_http_modsecurity_module.so;
```

### varnish-modules

Built against varnish 6.0 LTS from official RPM repository.

### libvmod-security

Built against varnish 6.0 LTS from official RPM repository.


Brought to life by<br/>
<a href="https://creativestyle.de">
	<img src="http://www.creativestyle.pl/wp-content/uploads/2014/04/CS-logo-red-creativestyle-gmbh-sp-z-o-o-interactive-agency-krakow-munchen-logo.png" width="150"/>
</a>