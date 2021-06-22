%define debug_package %{nil}

Name:           pushprox-client
Version:        0.1.0
Release:        1%{?dist}
Summary:        Proxy to allow Prometheus to scrape through NAT etc.

License:        Apache-2.0
URL:            https://github.com/prometheus-community/PushProx
Source0:        https://github.com/prometheus-community/PushProx/releases/download/v%{version}/PushProx-%{version}.linux-amd64.tar.gz
Source1:        https://github.com/prometheus-community/PushProx/releases/download/v%{version}/PushProx-%{version}.linux-arm64.tar.gz
Source2:        https://github.com/prometheus-community/PushProx/releases/download/v%{version}/PushProx-%{version}.linux-386.tar.gz
Source3:        %{name}.service
Source4:        %{name}.default


Requires(pre): shadow-utils
%{?systemd_requires}

%description
PushProx is a client and proxy that allows transversing of NAT and other similar network topologies by Prometheus, while still following the pull model.

%prep
%ifarch x86_64
%setup -q -b 0 -n PushProx-%{version}.linux-amd64
%endif
%ifarch aarch64
%setup -q -b 1 -n PushProx-%{version}.linux-arm64
%endif
%ifarch i386
%setup -q -b 2 -n PushProx-%{version}.linux-386
%endif

%build
true

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 pushprox-client %{buildroot}%{_bindir}/pushprox-client
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
%{_bindir}/pushprox-client
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}

%changelog
* Tue Oct 27 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Created package
