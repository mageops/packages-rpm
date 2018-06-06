Summary: WAF security shared library
Name: libmodsecurity
Version: 3.0.2
Release: 1%{?dist}
Group: System Environment/Libraries
Vendor: SpiderLabs
URL: https://github.com/SpiderLabs/ModSecurity

Requires: flex
Requires: bison
Requires: yajl
Requires: curl
Requires: zlib
Requires: pcre
BuildRequires: libcurl-devel
BuildRequires: flex
BuildRequires: bison
BuildRequires: curl-devel
BuildRequires: GeoIP-devel
BuildRequires: doxygen
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: yajl
BuildRequires: yajl-devel

Source0: https://github.com/SpiderLabs/ModSecurity/releases/download/v%{version}/modsecurity-v%{version}.tar.gz
Source1: https://github.com/SpiderLabs/ModSecurity/releases/download/v%{version}/modsecurity-v%{version}.tar.gz.asc

License: Apache License 2.0

BuildRoot: %{_tmppath}/%{name}-%{version}%{release}-root

%description
Shared library for ModSecurity WAF.

%package devel
Summary: libmodsecurity headers
Group: System Environment/Libraries
Requires: libmodsecurity

%description devel
Includes for ModSecurity WAF library.

%prep
%setup -q -n modsecurity-v%{version}

%build
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
%_libdir/%{name}*
%_bindir/modsec-rules-check

%files devel
%_includedir/*

