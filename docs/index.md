---
layout: default
title: Home
permalink: /
nav_order: 1
---

# Extra RPM packages for bleeding-edge cloud infrastructure
{: .fs-9 }

A **MageOps** RPM package collection sources, repository
and build automation.

{: .fs-6 .fw-300 }

[Use it now](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [View project on GitHub](https://github.com/mageops/packages-rpm){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Getting started

### Compatibility

This repository works in **CentOS/RHEL 7** and requires **EPEL** to be installed and enabled.

{: .text-grey-dk-000 }
Certain packages may require other repositories, the extra dependecies will be listed in
their description on this site.

### Install EPEL (required)

If you're on CentOS it should be sufficient to install it
from official release.

```shell
yum -y install epel-release
yum-config-manager --enable epel
```

### Direct RPM release package installation (recommended)

```shell
rpm -Uvh https://mageops.github.io/packages-rpm/repo/el/7/mageops-release.noarch.rpm
```

### Manual configuration by curl download (advanced)

1. Install the GPG signing key
```bash
curl -s https://raw.githubusercontent.com/mageops/packages-rpm/master/rpm-gpg-key.pub.asc > /etc/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS
```

2. Install the YUM repository config
```bash
curl -s https://raw.githubusercontent.com/mageops/packages-rpm/master/packages/mageops-release/mageops.repo > /etc/yum.repos.d/mageops.repo
```

### Finishing steps (optional)

1. Import the GPG signing key 
```bash
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS
```

2. Compute cache for the new repository
```bash
yum makecache --disablerepo="*" --enablerepo="mageops"
```



