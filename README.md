MageOps RPM package build
=========================

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
