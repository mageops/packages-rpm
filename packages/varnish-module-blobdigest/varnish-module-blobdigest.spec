Name:             varnish-module-blobdigest
Version:          1.1
Release:          9.6.0.12%{?dist}

Group:            System Environment/Libraries
Summary:          Varnish module (VMOD) for digests and hmacs with the VCL data type BLOB
License:          Public Domain

Vendor:           uplex
URL:              https://code.uplex.de/uplex-varnish/libvmod-blobdigest/tree/6.0

Source0:          https://code.uplex.de/uplex-varnish/libvmod-blobdigest/-/archive/6.0/libvmod-blobdigest-6.0.tar.bz2

Requires:         varnish = 6.0.12

BuildRequires:    varnish-devel = 6.0.12
BuildRequires:    perl >= 5
BuildRequires:    gcc, automake, libtool, python3, python-docutils

%description
Varnish module (VMOD) for digests and hmacs with the VCL data type BLOB

%prep
%setup -q -n libvmod-blobdigest-6.0

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
%license %{_datadir}/doc/libvmod-blobdigest/LICENSE
%doc %{_datadir}/doc/libvmod-blobdigest/*
%{_libdir}/varnish/vmods/libvmod_blobdigest.la
%{_libdir}/varnish/vmods/libvmod_blobdigest.so
%{_mandir}/man3/vmod_blobdigest*


%changelog
* Thu Feb 22 2024 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.1-9.6.0.12
- rebuilt

* Fri Dec 01 2023 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.1-8.6.0.11
- update varnish

* Thu Jan 27 2022 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.1-8.6.0.10
- update varnish

* Thu Nov 25 2021 Piotr Rogowski <piotrekrogowski@gmail.com> - 1.1-8.6.0.9
- update varnish

* Tue Jul 20 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.1-8.6.0.8
- Bump varnish dependency

* Wed Jun 23 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.1-8.0.7.1
- rebuilt

* Wed Jun 23 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.1-7.0.7.1
- rebuilt

* Mon Mar 29 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.1-6.0.7.1
- Initial release
