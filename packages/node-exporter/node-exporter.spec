%define debug_package %{nil}

Name:           node-exporter
Version:        1.0.1
Release:        3%{?dist}
Summary:        Exporter for machine metrics

License:        Apache-2.0
URL:            https://github.com/prometheus/node_exporter
Source0:        https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-amd64.tar.gz
Source1:        https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-arm64.tar.gz
Source2:        https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-386.tar.gz
Source3:        %{name}.service
Source4:        %{name}.default

Requires(pre): shadow-utils
%{?systemd_requires}

%description
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.

%prep
%ifarch x86_64
%setup -q -b 0 -n node_exporter-%{version}.linux-amd64
%endif
%ifarch aarch64
%setup -q -b 1 -n node_exporter-%{version}.linux-arm64
%endif
%ifarch i386
%setup -q -b 2 -n node_exporter-%{version}.linux-386
%endif

%build
true

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 node_exporter %{buildroot}%{_bindir}/node_exporter
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/default/%{name}

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
%doc NOTICE
%{_bindir}/node_exporter
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}

%changelog
* Thu Feb 22 2024 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.0.1-3
- rebuilt

* Thu Oct 29 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.0.1-2
- Fix environment file path

* Tue Oct 27 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Created package
