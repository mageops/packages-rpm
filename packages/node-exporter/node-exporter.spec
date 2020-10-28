%define debug_package %{nil}

Name:           node-exporter
Version:        1.0.1
Release:        1%{?dist}
Summary:        Exporter for machine metrics

License:        Apache-2.0
URL:            https://github.com/prometheus/node_exporter
%ifarch x86_64
Source0:        https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-amd64.tar.gz
%endif
%ifarch aarch64
Source0:        https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-arm64.tar.gz
%endif
%ifarch i386
Source0:        https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-386.tar.gz
%endif
Source1:        %{name}.service
Source2:        %{name}.default

Requires(pre): shadow-utils
%{?systemd_requires}

%description
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.

%prep
%ifarch x86_64
%setup -q -n node_exporter-%{version}.linux-amd64
%endif
%ifarch aarch64
%setup -q -n node_exporter-%{version}.linux-arm64
%endif
%ifarch i386
%setup -q -n node_exporter-%{version}.linux-386
%endif

%build
true

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 node_exporter %{buildroot}%{_bindir}/node_exporter
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
%doc NOTICE
%{_bindir}/node_exporter
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}

%changelog
* Tue Oct 27 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Created package
