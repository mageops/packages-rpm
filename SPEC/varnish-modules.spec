Summary: Official Varnish Modules Collection
Name: varnish-modules
Version: 0.15.0
Release: 1%{?dist}
Requires: varnish >= 4.1
Group: System Environment/Libraries
Vendor: varnish
URL: https://github.com/varnish/varnish-modules

Source0: https://github.com/varnish/varnish-modules/archive/0.15.0.tar.gz

License: BSD

BuildRoot: %{_tmppath}/%{name}-%{version}%{release}-root
BuildRequires: varnish-devel >= 4.1
BuildRequires: libtool

%if 0%{?amzn} == 1
BuildRequires: python27-docutils
%endif%

BuildRequires: python-docutils

%description
Official collection of varnish modules

%prep
%setup

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



