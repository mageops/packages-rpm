---
layout: default
title: Varnish Extras
permalink: /packages/varnish
parent: Packages
nav_order: 2
---

# Extras for Varnish Cache Server

These packages are meant to be used with latest LTS Varnish version
that has been installed from the official repositories.
{: .fs-6 .fw-300 }

### Install Varnish Official Repository

If you intend to use anu of this packages it's best that you have
you should have Varnish 6.0 LTS.

The most convenient way to make it avaialble
is to install the [Official Varnish Cache Repositories](https://packagecloud.io/varnishcache) 
we have [packaged](https://mageops.github.io/rpm/repo/el/7/varnish-release.noarch.rpm).

This will automatically enable the correct repository for the currently supported latest LTS version.

```bash
yum -y install varnish-release
```