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

[Get started now](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub](https://github.com/mageops/rpm){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Getting started

### Compatibility

This repository works in **CentOS/RHEL 7** withe **EPEL** installed.

Certain packages may require other repositories.

### Install EPEL (required)

If you're on CentOS it should be sufficient to install it
from official release.

```shell
yum -y install epel-release
yum-config-manager --enable epel
```

### Direct RPM release package installation (recommended)

```shell
rpm -Uvh https://mageops.github.io/rpm/repo/el/7/x86_64/mageops-release-7-1.noarch.rpm
```

### Manual configuration by curl download (advanced)

1. Install the GPG signing key
```bash
curl -s https://raw.githubusercontent.com/mageops/rpm/master/rpm-gpg-key.pub.asc > /etc/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS
```

2. Install the YUM repository config
```bash
curl -s https://raw.githubusercontent.com/mageops/rpm/master/packages/mageops-release/mageops.repo > /etc/yum.repos.d/mageops.repo
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

<!-- ### Manual configuration by pasting contents (advanced)

1. Place into `/etc/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS` file
```
{% include src/rpm-gpg-key.pub.asc %}
```

2. Paste into `/etc/yum.repos.d/mageops.repo` file
```ini
{% include src/packages/mageops-release/mageops.repo %}
``` -->
