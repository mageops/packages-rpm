%define debug_package %{nil}

Name:           php-fpm-exporter
Version:        0.6.1
Release:        1%{?dist}
Summary:        Prometheus exporter for php-fpm status.

License:        MIT
URL:            https://github.com/bakins/php-fpm-exporter
%ifarch x86_64
Source0:        https://github.com/bakins/php-fpm-exporter/releases/download/v%{version}/php-fpm-exporter.linux.amd64
%endif
Source1:        %{name}.service
Source2:        %{name}.default

Requires(pre): shadow-utils
%{?systemd_requires}

%description
Export php-fpm metrics in Prometheus format.

%prep
true

%build
true

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 %{SOURCE0} %{buildroot}%{_bindir}/php-fpm-exporter
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

%pre
getent group monitoring >/dev/null || groupadd -r monitoring
getent passwd monitoring >/dev/null || \
    useradd -r -g monitoring -d / -s /sbin/nologin \
    -c "Monitoring services" monitoring
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%{_bindir}/php-fpm-exporter
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}

%changelog
* Thu Oct 29 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Created package
