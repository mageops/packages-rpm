Summary: Official Varnish Modules Collection
Name: varnish-modules-mageops
Version: 0.15.0
Release: 1%{?dist}
Requires: varnish >= 6.0
Group: System Environment/Libraries
Vendor: varnish
URL: https://github.com/varnish/varnish-modules

Source0: https://github.com/varnish/varnish-modules/archive/0.15.0.tar.gz

License: BSD

Obsoletes:          %{name} <= %{version}
Obsoletes:          varnish-modules <= %{version}
Provides:           %{name}= %{version}
Provides:           varnish-modules= %{version}

BuildRoot: %{_tmppath}/%{name}-%{version}%{release}-root
BuildRequires: varnish-devel >= 6.0
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


%changelog
* Mon Nov 18 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 6.0
- Suffix package name with `-mageops`
- Compile against varnish 6.0 LTS



