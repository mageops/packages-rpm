---
layout: default
title: Unison File Sync
permalink: /packages/unison
parent: Packages
nav_order: 4
---

# Package collection for stable and fast two-way file synchronization

These packages have been crafted for providing two-way file synchronization
between host OS and virtualized (local or remote) development environment.
{: .fs-6 .fw-300 }

### Why

[Unison](https://github.com/bcpierce00/unison) is special in the way that it needs 
to be (preferably) the exact same version both on the host and guest. 

Not only that but also **it's best if has been compiled by the same version of _OCaml_**
due to BC breaks in serialization format across versions.

In order to achieve good stability we need to to maintain a compatible set of _unison_ 
binaries across all OSes - hence - we need to compile _unison_ using specfic
version of _OCaml_.

### Compatible binaries for other Operating Systems

#### MacOS

The latest version from [brew](https://brew.sh/) is the one that we wanted to stay
compatible with.

```bash
brew install unison
```

#### Windows

Sorry, we don't support _Windows_ **yet**. Stay tuned! 🤟
