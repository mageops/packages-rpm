Images for building RPM packages for CentOS/Amilinux
====================================================

## Deprecation Warning

**This dockerfiles are deprecated and not maintained anymore as now we use Fedora COPR for building the packages.** This files are left here only for reference and may be useful for locally testing the builds later on.

## Build images

You shall have docker for that:

```
./build-images.sh
```

You can also use prebuilt images from our repo:

`docker.creativestyle.pl:5050/m2c/cs-rpm-build`

Where the tags are:
  - amilinux-1
  - amilinux-2
  - centos-6
  - centos-7

## Build rpm package

Your package sources should be in the working directory, mount it
as /rpbuild. Then do docker exec with the only argument being specfile
path.

```
docker run --rm -v "$PWD":/root/rpmbuild cs-rpm-build-amilinux-1 SPEC/nginx.spec
```

See `build-rpm.sh` for the whole RPM build process.

If you place GPG public keys in `signing_keys` subdirectory with `*.key`
extension then they will be imported. Any `SOURCES/*.asc` file will be
automatically verified using GPG.