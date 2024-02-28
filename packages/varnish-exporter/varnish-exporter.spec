%define debug_package %{nil}
%define commit_sha 86fc1b025dd41eaf43a583a262daec6cad69b561

Name:           varnish-exporter
Version:        1.6.1
Release:        1%{?dist}
Summary:        Varnish exporter for Prometheus

License:        MIT License
URL:            https://github.com/jonnenauha/prometheus_varnish_exporter
Source0:        https://github.com/jonnenauha/prometheus_varnish_exporter/archive/%{commit_sha}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.default
Requires:       varnish
Requires(pre):  shadow-utils
BuildRequires:  golang
%{?systemd_requires}

%description
Varnish exporter for Prometheus

%prep
%setup -q -n prometheus_varnish_exporter-%{commit_sha}

%build
export GOPROXY="https://proxy.golang.org"
export GO111MODULE=on
export VERSION="%{version}"
export VERSION_HASH="%{commit_sha}"
export VERSION_DATE="$(date -u '+%%d.%%m.%%Y %%H:%%M:%%S')"
go build -o prometheus_varnish_exporter  -ldflags "-X 'main.Version=$VERSION' -X 'main.VersionHash=$VERSION_HASH' -X 'main.VersionDate=$VERSION_DATE'"

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
* Fri May 14 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.6.1-1
- New version build from master

* Mon Feb 15 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.6-1
- new version

* Thu Oct 29 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.5.2-2
- Add dependency to varnish, also service need to be executed with varnish group

* Wed Oct 28 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Created package
