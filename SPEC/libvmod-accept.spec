Summary: Varnish Accept VMOD
Name: libvmod-accept
Version: 4.1
Release: 1%{?dist}
Requires: varnish >= 4.1
Group: System Environment/Libraries
Vendor: gquintard
URL: https://github.com/gquintard/libvmod-accept

Source0: https://github.com/creativestyle/libvmod-accept/archive/4.1.tar.gz

License: Public Domain

BuildRoot: %{_tmppath}/%{name}-%{version}%{release}-root
BuildRequires: varnish-devel >= 4.1
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
make %{?_smp_mflags}

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


