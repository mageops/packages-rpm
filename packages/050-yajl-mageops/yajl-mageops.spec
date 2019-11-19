Summary: YAJL JSON Parser
Name: yajl-mageops
Version: 2.1.0
Release: 1%{?dist}
Group: System Environment/Libraries
Vendor: lloyd
URL: https://lloyd.github.io/yajl/

BuildRequires: gcc
BuildRequires: cmake

Obsoletes:          %{name} <= %{version}
Obsoletes:          yajl <= %{version}
Provides:           %{name}= %{version}
Provides:           yajl= %{version}

Source0: https://github.com/lloyd/yajl/archive/%{version}.tar.gz

License: ISC

BuildRoot: %{_tmppath}/%{name}-%{version}%{release}-root

%description
JSON parsing library.

%package devel
Summary: yajl headers
Group: System Environment/Libraries
Requires: yajl

%description devel
Includes for yajl

%prep
%setup -q -n yajl-%{version}

%build

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
      -DLIB_SUFFIX="64" \
      ..
make %{?_smp_mflags}

%install
cd build
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%_libdir/libyajl*
%_bindir/json_reformat
%_bindir/json_verify
%_prefix/share/pkgconfig/yajl.pc

%files devel
%_includedir/*

