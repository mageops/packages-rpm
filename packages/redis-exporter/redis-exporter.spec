%define debug_package %{nil}

Name:           redis-exporter
Version:        1.13.1
Release:        1%{?dist}
Summary:        Prometheus Exporter for Redis Metrics. Supports Redis 2.x, 3.x, 4.x, 5.x and 6.x

License:        MIT
URL:            https://github.com/oliver006/redis_exporter
%ifarch x86_64
Source0:        https://github.com/oliver006/redis_exporter/releases/download/v%{version}/redis_exporter-v%{version}.linux-amd64.tar.gz
%endif
%ifarch aarch64
Source0:        https://github.com/oliver006/redis_exporter/releases/download/v%{version}/redis_exporter-v%{version}.linux-arm64.tar.gz
%endif
%ifarch i386
Source0:        https://github.com/oliver006/redis_exporter/releases/download/v%{version}/redis_exporter-v%{version}.linux-386.tar.gz
%endif
Source1:        %{name}.service
Source2:        %{name}.default

Requires(pre): shadow-utils
%{?systemd_requires}

%description
Prometheus exporter for Redis metrics.
Supports Redis 2.x, 3.x, 4.x, 5.x, and 6.x

%prep
%ifarch x86_64
%setup -q -n redis_exporter-v%{version}.linux-amd64
%endif
%ifarch aarch64
%setup -q -n redis_exporter-v%{version}.linux-arm64
%endif
%ifarch i386
%setup -q -n redis_exporter-v%{version}.linux-386
%endif


%build
true

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 redis_exporter %{buildroot}%{_bindir}/redis_exporter
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
%doc README.md
%{_bindir}/redis_exporter
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}

%changelog
* Tue Nov  3 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Created package
