Summary: Varnish Accept Header Module
Name: varnish-module-accept-mageops
Version: 6.0
Release: 1%{?dist}
Requires: varnish >= 6.0
Group: System Environment/Libraries
Vendor: gquintard
URL: https://github.com/gquintard/libvmod-accept

Source0: https://github.com/gquintard/libvmod-accept/archive/6.0.tar.gz

License: Public Domain

Obsoletes:          %{name} <= %{version}
Obsoletes:          libvmod-accept <= %{version}
Provides:           %{name}= %{version}
Provides:           libvmod-accept= %{version}

BuildRoot: %{_tmppath}/%{name}-%{version}%{release}-root
BuildRequires: varnish-devel >= 6.0
BuildRequires: libtool

%if 0%{?amzn} == 1
BuildRequires: python27-docutils
%endif%

BuildRequires: python-docutils

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
* Mon Nov 18 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 6.0
- Compile against varnish 6.0 LTS
- Switch back to original repository source
- Suffix package name with `-mageops`