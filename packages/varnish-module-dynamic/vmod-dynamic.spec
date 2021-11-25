# -D MUST pass in _version and _release, and SHOULD -pass in dist.

%global vmod    dynamic
%global vmoddir %{_libdir}/varnish/vmods
%global varnish_lock 6.0.9
%global commit b72c723acff5b2ef46c9de8cef036cee3a380a64

Name:           varnish-module-%{vmod}
Version:        0.4
Release:        2.%{varnish_lock}%{?dist}
Group:          System Environment/Libraries
Summary:        DNS director for Varnish Cache
URL:            https://github.com/nigoroll/libvmod-dynamic
License:        BSD
Source0:         https://github.com/nigoroll/libvmod-dynamic/archive/%{commit}.tar.gz

BuildRequires:  varnish-devel = %{varnish_lock}
BuildRequires:  pkgconfig
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  getdns-devel
BuildRequires:  python-docutils >= 0.6

Requires:       getdns
Requires:       varnish = %{varnish_lock}

Provides: %{name}, %{name}-debuginfo

%description
A VMOD to create dynamic director, that is to say relying on DNS to dynamically
create backends.


%prep
%setup -qn libvmod-dynamic-%{commit}


%build
./autogen.sh
%configure
# It do not build in parralel
make -j1

%install
%make_install
rm %{buildroot}%{vmoddir}/libvmod_%{vmod}.la

# Only use the version-specific docdir created by %doc below
#rm -rf %{buildroot}%{_docdir}

# Disable some racy tests
# %check
# # Skip test03 because it have race confition in delay, depending on hardware speed
# ls src/tests/test*
# echo 'varnishtest "skipped"' | tee src/tests/test03.vcl
# # Skip test13 because it fails without changes to hosts configuration
# echo 'varnishtest "skipped"' | tee src/tests/test13.vcl
# cat src/tests/test03.vcl src/tests/test13.vcl
# make %{?_smp_mflags} check


%files
%{vmoddir}/libvmod_%{vmod}.so
%{_mandir}/man?/*
%doc %_docdir/vmod-dynamic/*


%changelog
* Thu Nov 25 2021 Piotr Rogowski <piotrekrogowski@gmail.com> - 0.4-2.6.0.9
- update varnish

* Tue Aug 03 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 0.4-2.6.0.8
- Update to never revision

* Mon Jul 19 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 0.4-1
- Initial release
