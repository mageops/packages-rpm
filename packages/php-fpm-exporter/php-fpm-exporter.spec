%define debug_package %{nil}

Name:           php-fpm-exporter
Version:        1.1.1
Release:        1%{?dist}
Summary:        A prometheus exporter for PHP-FPM.

License:        MIT
URL:            https://github.com/hipages/php-fpm_exporter
%ifarch x86_64
Source0:        https://github.com/hipages/php-fpm_exporter/releases/download/v%{version}/php-fpm_exporter_%{version}_linux_amd64
%endif
Source1:        %{name}.service
Source2:        %{name}.default

Requires(pre): shadow-utils
%{?systemd_requires}

%description
A prometheus exporter for PHP-FPM. The exporter connects directly to PHP-FPM and exports the metrics via HTTP.

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
