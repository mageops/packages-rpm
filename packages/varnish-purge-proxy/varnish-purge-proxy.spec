
Name:             varnish-purge-proxy
Version:          3.0.1
Release:          1%{?dist}

Group:            Cloud Infrastructure/Tools
Summary:          Proxies purge requests to autodiscovered Varnish nodes
License:          GPLv3

Vendor:           David Watson <david@planetwatson.co.uk>
Packager:         creativestyle Polska <https://creativestyle.pl>
URL:              https://github.com/BashtonLtd/varnish-purge-proxy

Source0:          https://github.com/BashtonLtd/varnish-purge-proxy/releases/download/varnish-purge-proxy

BuildArch:        noarch


%description
A small daemon that proxies HTTP PURGE requests to multiple Varnish nodes that
are autodiscovered via cloud (AWS, GCP) infrastructure APIs.


%prep
%setup -q  -c -T

%install
mkdir -p %{buildroot}%{_bindir}

install -p -m 755 %{SOURCE0} %{buildroot}%{_bindir}/varnish-purge-proxy

%files
%defattr(-,root,root,-)
%{_bindir}/varnish-purge-proxy

%changelog
* Thu Nov 28 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 3.0.1-1
- Initial version




