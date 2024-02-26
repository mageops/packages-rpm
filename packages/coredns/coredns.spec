Name:           coredns
Version:        1.8.4
Release:        2%{?dist}
Summary:        CoreDNS is a DNS server that chains plugins


License:        Apache License 2.0
URL:            https://coredns.io/
Source0:        https://github.com/coredns/coredns/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  golang >= 1.13
Requires:       make
Requires:       git
%global debug_package %{nil}


%description
oreDNS is a DNS server/forwarder, written in Go, that chains plugins.
Each plugin performs a (DNS) function.
CoreDNS is a Cloud Native Computing Foundation graduated project.
CoreDNS is a fast and flexible DNS server. The key word here is flexible:
with CoreDNS you are able to do what you want with your DNS data by utilizing plugins.
If some functionality is not provided out of the box you can add it by writing a plugin.
CoreDNS can listen for DNS requests coming in over UDP/TCP (go'old DNS), TLS (RFC 7858),
also called DoT, DNS over HTTP/2 - DoH - (RFC 8484) and gRPC (not a standard).

%prep
%setup -q -n %{name}-%{version}
echo 'dynamic:github.com/mageops/coredns-dynamic' | tee -a plugin.cfg
export GOPROXY="https://goproxy.io,direct"
export GO111MODULE=on
go mod edit -require=github.com/mageops/coredns-dynamic@v0.0.0-20210723110350-1183bb7569e2
go mod download github.com/mageops/coredns-dynamic

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT%{_bindir}
install -pm 755 coredns $RPM_BUILD_ROOT%{_bindir}/coredns

%files
%license LICENSE
%doc README.md
%{_bindir}/coredns


%changelog
* Thu Feb 22 2024 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.8.4-2
- rebuilt

* Fri Jul 23 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Initial release
