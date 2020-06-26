%define nginx_version 1.18.0
Name:           nginx-module-geoip2
Version:        3.3
Release:        %{nginx_version}.1%{?dist}
Summary:        Nginx GeoIP2 module
Packager:       creativestyle GmbH <https://creativestyle.pl>

License:        BSD 2
URL:            https://github.com/leev/ngx_http_geoip2_module/
Source0:        https://github.com/leev/ngx_http_geoip2_module/archive/%{version}.tar.gz
Source1:        http://nginx.org/download/nginx-%{nginx_version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libmaxminddb-devel
Requires:       nginx = 1:1.18.0
Requires:       libmaxminddb

%description
creates variables with values from the maxmind geoip2 databases based on the client IP (default) or from a specific variable (supports both IPv4 and IPv6)

The module now supports nginx streams and can be used in the same way the http module can be used.

%prep
%setup -b 1 -q -n nginx-%{nginx_version}

%build
# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.
export DESTDIR=%{buildroot}
# So the perl module finds its symbols:
nginx_ldopts="$RPM_LD_FLAGS -Wl,-E"
./configure \
    --prefix=%{_datadir}/nginx \
    --sbin-path=%{_sbindir}/nginx \
    --modules-path=%{_libdir}/nginx/modules \
    --conf-path=%{_sysconfdir}/nginx/nginx.conf \
    --with-debug \
    --without-http_rewrite_module \
    --without-http_gzip_module \
    --with-cc-opt="%{optflags}" \
    --add-dynamic-module=../ngx_http_geoip2_module-3.3 \
    --with-ld-opt="$nginx_ldopts"

make modules %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}/nginx/modules/
cp objs/ngx_http_geoip2_module.so %{buildroot}%{_libdir}/nginx/modules/

%files
%license ../ngx_http_geoip2_module-3.3/LICENSE
%{_libdir}/nginx/modules/ngx_http_geoip2_module.so


%changelog
* Thu Jun 25 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
-
