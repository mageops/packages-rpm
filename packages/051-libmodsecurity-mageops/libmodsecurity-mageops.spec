Summary: WAF security shared library
Name: libmodsecurity-mageops
Version: 3.0.2
Release: 1%{?dist}
Group: System Environment/Libraries
Vendor: SpiderLabs
URL: https://github.com/SpiderLabs/ModSecurity

Requires: flex
Requires: bison
Requires: yajl-mageops
Requires: curl
Requires: zlib
Requires: pcre
Requires: ssdeep-libs
Requires: libxml2
Requires: GeoIP
BuildRequires: libcurl-devel
BuildRequires: flex
BuildRequires: bison
BuildRequires: curl-devel
BuildRequires: GeoIP-devel
BuildRequires: doxygen
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: ssdeep-libs
BuildRequires: ssdeep-devel
BuildRequires: libxml2
BuildRequires: libxml2-devel
BuildRequires: yajl-mageops-devel

Obsoletes:          %{name} <= %{version}
Obsoletes:          libmodsecurity <= %{version}
Provides:           %{name}= %{version}
Provides:           libmodsecurity= %{version}

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

