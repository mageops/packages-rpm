%define modsec_nginx_version 1.0.0
%define modsec_nginx_name modsecurity-nginx-v%{modsec_nginx_version}

%define pagespeed_version 1.13.35.2
%define pagespeed_name incubator-pagespeed-ngx-%{pagespeed_version}-stable

%define use_systemd 0%{?rhel} && 0%{?rhel} >= 7

%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define nginx_loggroup adm


%if 0%{?rhel}  == 6
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Requires: systemd
BuildRequires: systemd
%endif%

Summary: High performance web server
Group: System Environment/Daemons
Name: nginx-mageops
Version: 1.13.5
Release: 1%{?dist}
Vendor: nginx inc.
URL: http://nginx.org/
Epoch: 1

Obsoletes:          %{name} <= %{version}
Obsoletes:          nginx-creativeshop <= %{version}

Conflicts:          nginx

Requires(pre):      shadow-utils
Requires:           openssl >= 1.0.1
Requires:           libcurl
Requires:           libxml2

BuildRequires:      openssl-devel >= 1.0.1
BuildRequires:      libcurl-devel
BuildRequires:      libxml2-devel
BuildRequires:      httpd
BuildRequires:      httpd-devel
BuildRequires:      flex
BuildRequires:      bison
BuildRequires:      GeoIP
BuildRequires:      unzip

%define with_http2 1

Source0: http://nginx.org/download/nginx-%{version}.tar.gz
Source1: http://nginx.org/download/nginx-%{version}.tar.gz.asc
Source2: logrotate
Source3: nginx.init
Source4: nginx.sysconf
Source5: nginx.conf
Source6: nginx.default.host
Source7: nginx-debug.sysconf
Source8: nginx.service
Source9: nginx.upgrade.sh
Source10: nginx-debug.service
Source11: https://github.com/SpiderLabs/ModSecurity-nginx/releases/download/v%{modsec_nginx_version}/%{modsec_nginx_name}.tar.gz
Source12: https://github.com/SpiderLabs/ModSecurity-nginx/releases/download/v%{modsec_nginx_version}/%{modsec_nginx_name}.tar.gz.asc
Source13: https://github.com/apache/incubator-pagespeed-ngx/archive/v%{pagespeed_version}-stable.tar.gz
Source14: https://dl.google.com/dl/page-speed/psol/%{pagespeed_version}-x64.tar.gz
Source15: nginx-modsecurity.conf
Source16: nginx-pagespeed.conf

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel

Provides: webserver

%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server.

%package debug
Summary: debug version of nginx
Group: System Environment/Daemons
Requires: nginx

%description debug
Not stripped version of nginx built with the debugging log support.

%package modsecurity
Summary: NGINX modsecurity module
Group: System Environment/Libraries
Requires: libmodsecurity-mageops

%description modsecurity
Libmodsecurity connector module for NGINX

%package pagespeed
Summary: NINX modsecurity module
Group: System Environment/Libraries
Requires: libuuid
BuildRequires: libuuid
BuildRequires: libuuid-devel

%description pagespeed
Libmodsecurity connector module for NGINX

%prep
%setup -q -n nginx-%{version}
%setup -q -T -D -a 11 -n nginx-%{version}
%setup -q -T -D -a 13 -n nginx-%{version}

%build

tar xzf %{SOURCE14} -C %{pagespeed_name}

./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-threads \
        --with-stream \
        --with-stream_ssl_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-pcre \
        --add-dynamic-module=%{_builddir}/nginx-%{version}/%{modsec_nginx_name} \
        --add-dynamic-module=%{_builddir}/nginx-%{version}/%{pagespeed_name} \
        %{?with_http2:--with-http_v2_module} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE6} \
  $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx
%{__install} -m 644 -p %{SOURCE7} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx-debug

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
    $RPM_BUILD_ROOT%{_unitdir}/nginx.service
%{__install} -m644 %SOURCE10 \
    $RPM_BUILD_ROOT%{_unitdir}/nginx-debug.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
%{__install} -m755 %SOURCE9 \
    $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}/nginx
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE2} \
    $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx/modules

# install module configs
%{__install} -m 644 -p %{SOURCE15} \
    $RPM_BUILD_ROOT%{_datadir}/nginx/modules/modsecurity.conf

%{__install} -m 644 -p %{SOURCE16} \
    $RPM_BUILD_ROOT%{_datadir}/nginx/modules/pagespeed.conf

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx-debug
%if %{use_systemd}
%{_unitdir}/nginx.service
%{_unitdir}/nginx-debug.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/nginx
%endif%endif

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%dir %{_datadir}/nginx/modules

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

%files modsecurity
%{_sysconfdir}/nginx/modules/ngx_http_modsecurity_module.so
%{_datadir}/nginx/modules/modsecurity.conf

%files pagespeed
%{_sysconfdir}/nginx/modules/ngx_pagespeed.so
%{_datadir}/nginx/modules/pagespeed.conf

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post
# Register the nginx service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using nginx!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

----------------------------------------------------------------------
BANNER

    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi

%changelog
* Mon Nov 18 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 6.0
- Suffix package name with `-mageops`
- Mark as upgrade from `nginx-creativeshop`
