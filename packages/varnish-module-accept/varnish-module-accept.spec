Name:             varnish-module-accept
Version:          6.0
Release:          2.6.0.7%{?dist}

Group:            System Environment/Libraries
Summary:          Varnish Accept Header Module
License:          Public Domain

Vendor:           gquintard
Packager:         creativestyle GmbH <https://creativestyle.de>
URL:              https://github.com/gquintard/libvmod-accept

Source0:          https://github.com/gquintard/libvmod-accept/archive/6.0.tar.gz

Conflicts:        libvmod-accept
Requires:         varnish = 6.0.7

BuildRoot:        %{_tmppath}/%{name}-%{version}%{release}-root
BuildRequires:    varnish-devel = 6.0.7
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
* Mon Dec 07 2020 Filip Sobalski <filip.sobalski@creativestyle.pl> - 6.0-2.6.0.7
- Bump release and deps to support new varnish 6.0.7

* Wed Feb 05 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 6.0-2.6.0.6
- Stick to specific version of varnish to prevent abi incompatibility

* Tue Nov 19 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 6.0
- Bump module varnish version
- Switch back to original sources
