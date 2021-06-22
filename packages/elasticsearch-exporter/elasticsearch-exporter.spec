%define debug_package %{nil}

Name:           elasticsearch-exporter
Version:        1.1.0
Release:        1%{?dist}
Summary:        Elasticsearch stats exporter for Prometheus

License:        MIT
URL:            https://github.com/justwatchcom/elasticsearch_exporter
Source0:        https://github.com/justwatchcom/elasticsearch_exporter/releases/download/v%{version}/elasticsearch_exporter-%{version}.linux-amd64.tar.gz
Source1:        https://github.com/justwatchcom/elasticsearch_exporter/releases/download/v%{version}/elasticsearch_exporter-%{version}.linux-arm64.tar.gz
Source2:        https://github.com/justwatchcom/elasticsearch_exporter/releases/download/v%{version}/elasticsearch_exporter-%{version}.linux-386.tar.gz
Source3:        %{name}.service
Source4:        %{name}.default

Requires(pre): shadow-utils
%{?systemd_requires}

%description
Prometheus exporter for various metrics about ElasticSearch, written in Go.

%prep
%ifarch x86_64
%setup -q -b 0 -n elasticsearch_exporter-%{version}.linux-amd64
%endif
%ifarch aarch64
%setup -q -b 1 -n elasticsearch_exporter-%{version}.linux-arm64
%endif
%ifarch i386
%setup -q -b 2 -n elasticsearch_exporter-%{version}.linux-386
%endif

%build
true

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 elasticsearch_exporter %{buildroot}%{_bindir}/elasticsearch_exporter
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
%doc README.md CHANGELOG.md
%{_bindir}/elasticsearch_exporter
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}

%changelog
* Mon Nov  2 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Created package
