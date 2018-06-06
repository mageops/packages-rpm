Builds customized & nginx and related modules RPMs for CentOS/AmazonLinux
=========================================================================

## Build

The script `build-thos-freaking-packages.sh` should be self-explanatory.

Packages are built using special docker images from here:
git@gitlab.creativestyle.pl:m2c/docker-aws-rpm-build-image.git

See the [jenkins jobs](http://m2ci.creativestyle.company:8080/view/automation/).

## Modsecurity

Libmodsecurity is compiled without LUA support as the RHEL version is too
old. No planned support for now.

Includes support for:
  - ssdeep
  - libxml2
  - GeoIP

## Nginx

Modules are dynamically linked. You need to load the module manually in your `nginx.conf`, e.g.:

```
    load_module modules/ngx_http_modsecurity_module.so;
```
