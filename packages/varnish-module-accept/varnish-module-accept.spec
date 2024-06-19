Name:             varnish-module-accept
Version:          6.0
Release:          6.6.0.13%{?dist}

Group:            System Environment/Libraries
Summary:          Varnish Accept Header Module
License:          Public Domain

Vendor:           gquintard
URL:              https://github.com/gquintard/libvmod-accept

Source0:          https://github.com/gquintard/libvmod-accept/archive/6.0.tar.gz

Conflicts:        libvmod-accept
Requires:         varnish = 6.0.13

BuildRoot:        %{_tmppath}/%{name}-%{version}%{release}-root
BuildRequires:    varnish-devel = 6.0.13
BuildRequires:    libtool
BuildRequires:    python-docutils

%description
Varnish module for accept header normalization.

%prep
%setup -q -n libvmod-accept-%{version}

%build
./autogen.sh
./configure --libdir=%{_libdir} \
            --prefix=%{_prefix} \
            --includedir=%{_includedir} \
            --bindir=%{_bindir}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%_libdir/varnish/vmods/libvmod_accept*
%_mandir/man3/vmod_accept*
%_datarootdir/doc/vmod-accept/*

%changelog
* Fri Dec 01 2023 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 6.0-6.6.0.12
- update varnish

* Thu Jan 27 2022 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 6.0-6.6.0.10
- update varnish

* Thu Nov 25 2021 Piotr Rogowski <piotrekrogowski@gmail.com> - 6.0-6.6.0.9
- update varnish

* Thu Nov 25 2021 Piotr Rogowski <piotrekrogowski@gmail.com> - 6.0-5.6.0.9
- update

* Tue Jul 20 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 6.0-4.6.0.8
- Bump varnish dependency

* Wed Jun 23 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 6.0-4.6.0.7
- rebuilt

* Wed Jun 23 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 6.0-3.6.0.7
- rebuilt

* Mon Dec 07 2020 Filip Sobalski <filip.sobalski@creativestyle.pl> - 6.0-2.6.0.7
- Bump release and deps to support new varnish 6.0.7

* Wed Feb 05 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 6.0-2.6.0.6
- Stick to specific version of varnish to prevent abi incompatibility

* Tue Nov 19 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 6.0
- Bump module varnish version
- Switch back to original sources
