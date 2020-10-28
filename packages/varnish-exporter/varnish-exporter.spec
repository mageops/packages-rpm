%define debug_package %{nil}

Name:           varnish-exporter
Version:        1.5.2
Release:        1%{?dist}
Summary:        Varnish exporter for Prometheus

License:        MIT License
URL:            https://github.com/jonnenauha/prometheus_varnish_exporter
%ifarch x86_64
Source0:        https://github.com/jonnenauha/prometheus_varnish_exporter/releases/download/%{version}/prometheus_varnish_exporter-%{version}.linux-amd64.tar.gz
%endif
%ifarch i386
Source0:        https://github.com/jonnenauha/prometheus_varnish_exporter/releases/download/%{version}/prometheus_varnish_exporter-%{version}.linux-386.tar.gz
%endif
Source1:        %{name}.service
Source2:        %{name}.default

Requires(pre): shadow-utils
%{?systemd_requires}

%description
Varnish exporter for Prometheus

%prep
%ifarch x86_64
%setup -q -n prometheus_varnish_exporter-%{version}.linux-amd64
%endif
%ifarch i386
%setup -q -n prometheus_varnish_exporter-%{version}.linux-386
%endif

%build
true

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 prometheus_varnish_exporter %{buildroot}%{_bindir}/prometheus_varnish_exporter
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
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/prometheus_varnish_exporter
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}

%changelog
* Wed Oct 28 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Created package
