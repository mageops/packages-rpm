Name:             varnish-modules-extra
Version:          0.15.0
Release:          3.6.0.7%{?dist}

Group:            System Environment/Libraries
Summary:          Varnish Official Module Collection
License:          BSD

Vendor:           varnish
URL:              https://github.com/varnish/varnish-modules

Source0:          https://github.com/varnish/varnish-modules/archive/0.15.0.tar.gz

Conflicts:        varnish-modules
Requires:         varnish = 6.0.7

BuildRoot:        %{_tmppath}/%{name}-%{version}%{release}-root
BuildRequires:    varnish-devel = 6.0.7
BuildRequires:    libtool
BuildRequires:    python-docutils

%description
Official collection of varnish modules

%prep
%setup -q -n varnish-modules-%{version}

%build
./bootstrap
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
%_libdir/varnish/vmods/*
%_mandir/man3/*
%_datarootdir/doc/v*

%changelog
* Wed Jun 23 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 0.15.0-3.6.0.7
- rebuilt

* Wed Jun 23 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 0.15.0-2.6.0.7
- rebuilt

* Mon Dec 07 2020 Filip Sobalski <filip.sobalski@creativestyle.pl> - 0.15.0-1.6.0.7
- Bump release and deps to support new varnish 6.0.7

* Wed Feb 05 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 0.15.0-1.6.0.6
- Stick to specific version of varnish to prevent abi incompatibility

* Tue Nov 19 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 6.0
- Bump version
