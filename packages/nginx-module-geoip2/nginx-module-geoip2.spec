%define nginx_version 1.20.2
%define nginx_user nginx
%define nginx_group nginx

Name:           nginx-module-geoip2
Version:        3.3
Release:        %{nginx_version}.4%{?dist}
Summary:        Nginx GeoIP2 module
Packager:       creativestyle GmbH <https://creativestyle.pl>

License:        BSD 2
URL:            https://github.com/leev/ngx_http_geoip2_module/
Source0:        https://github.com/leev/ngx_http_geoip2_module/archive/%{version}.tar.gz
Source1:        http://nginx.org/download/nginx-%{nginx_version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libmaxminddb-devel
BuildRequires:  zlib-devel
BuildRequires:  pcre-devel
BuildRequires:  openssl-devel
Requires:       nginx = 1:%{nginx_version}
Requires:       libmaxminddb

%description
creates variables with values from the maxmind geoip2 databases based on the client IP (default) or from a specific variable (supports both IPv4 and IPv6)

The module now supports nginx streams and can be used in the same way the http module can be used.

%define WITH_CC_OPT $(echo %{optflags} $(pcre-config --cflags))
%define WITH_LD_OPT -Wl,-z,relro -Wl,-z,now

%define BASE_CONFIGURE_ARGS $(echo "--prefix=%{_sysconfdir}/nginx --sbin-path=%{_sbindir}/nginx --modules-path=%{_libdir}/nginx/modules \
    --conf-path=%{_sysconfdir}/nginx/nginx.conf --error-log-path=%{_localstatedir}/log/nginx/error.log \
    --http-log-path=%{_localstatedir}/log/nginx/access.log --pid-path=%{_localstatedir}/run/nginx.pid \
    --lock-path=%{_localstatedir}/run/nginx.lock --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
    --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
    --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp --user=%{nginx_user} \
    --group=%{nginx_group} --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module \
    --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module \
    --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module \
    --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail \
    --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module")
%define MODULE_CONFIGURE_ARGS $(echo "")

%prep
%setup -b 1 -q -n nginx-%{nginx_version}

%build
./configure %{BASE_CONFIGURE_ARGS} %{MODULE_CONFIGURE_ARGS} \
        --with-cc-opt="%{WITH_CC_OPT} " \
        --with-ld-opt="%{WITH_LD_OPT} " \
        --with-debug \
        --add-dynamic-module=../ngx_http_geoip2_module-3.3

make %{?_smp_mflags} modules

%install
mkdir -p %{buildroot}%{_libdir}/nginx/modules/
cp objs/ngx_http_geoip2_module.so objs/ngx_stream_geoip2_module.so %{buildroot}%{_libdir}/nginx/modules/

%files
%license ../ngx_http_geoip2_module-3.3/LICENSE
%{_libdir}/nginx/modules/ngx_http_geoip2_module.so
%{_libdir}/nginx/modules/ngx_stream_geoip2_module.so


%changelog
* Thu Dec 09 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 3.3-1.20.2.4
- Update nginx version

* Thu Sep 02 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 3.3-1.20.1.4
- Update nginx version

* Fri Jun 26 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 3.3-1.18.0.4
- Add explicit flags for compatibility and add stream module

* Fri Jun 26 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 3.3-1.18.0.3
- Add compat flag to configure

* Fri Jun 26 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 3.3-1.18.0.2
- fix nginx version

* Thu Jun 25 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Initial build
