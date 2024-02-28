%define debug_package %{nil}

Name:           php-fpm-exporter
Version:        2.0.1
Release:        1%{?dist}
Summary:        A prometheus exporter for PHP-FPM.

License:        MIT
URL:            https://github.com/hipages/php-fpm_exporter
Source0:        https://github.com/hipages/php-fpm_exporter/releases/download/v%{version}/php-fpm_exporter_%{version}_linux_amd64
Source1:        https://github.com/hipages/php-fpm_exporter/releases/download/v%{version}/php-fpm_exporter_%{version}_linux_arm64
Source2:        %{name}.service
Source3:        %{name}.default

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
%ifarch x86_64
install -D -m 755 %{SOURCE0} %{buildroot}%{_bindir}/php-fpm-exporter
%endif
%ifarch aarch64
install -D -m 755 %{SOURCE1} %{buildroot}%{_bindir}/php-fpm-exporter
%endif
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/default/%{name}

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
* Mon Feb 15 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 2.0.1-1
- new version

* Thu Oct 29 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Created package
