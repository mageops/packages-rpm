%ifarch %{ocaml_native_compiler}
%global native_compiler 1
%else
%global native_compiler 0
%global debug_package %{nil}
%endif

# Upstream has been deprecated, but still supports OCaml 4.08.
%global commit 6cb56649d294092d0da55fda095738b330772520
%global shortcommit 6cb56649

Name:          ocaml-camlp4
Version:       4.08.1
Release:       1.git%{shortcommit}%{?dist}

Summary:       Pre-Processor-Pretty-Printer for OCaml

License:       LGPLv2+ with exceptions

URL:           https://github.com/ocaml/camlp4
Source0:       https://github.com/ocaml/camlp4/archive/%{commit}.tar.gz

BuildRequires: ocaml-ocamlbuild

# This package used to be part of the upstream compiler.  We still
# need to keep it in lock step with the compiler, so whenever a new
# compiler is released we will also update this package also.
BuildRequires: ocaml = %{version}
Requires:      ocaml-runtime = %{version}


%description
Camlp4 is a Pre-Processor-Pretty-Printer for OCaml, parsing a source
file and printing some result on standard output.

This package contains the runtime files.


%package devel
Summary:       Pre-Processor-Pretty-Printer for OCaml

Requires:      %{name}%{?_isa} = %{version}-%{release}


%description devel
Camlp4 is a Pre-Processor-Pretty-Printer for OCaml, parsing a source
file and printing some result on standard output.

This package contains the development files.


%prep
%setup -q -n camlp4-%{commit}


%build
./configure

# Incompatible with parallel builds.
unset MAKEFLAGS
%if !%{native_compiler}
make byte
%else
make all
%endif


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/camlp4
make install \
  BINDIR=$RPM_BUILD_ROOT%{_bindir} \
  LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
  PKGDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/camlp4


%files
%doc README.md LICENSE
%dir %{_libdir}/ocaml/camlp4
%{_libdir}/ocaml/camlp4/*.cmi
%{_libdir}/ocaml/camlp4/*.cma
%{_libdir}/ocaml/camlp4/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Filters
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Parsers
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmo
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmi
%dir %{_libdir}/ocaml/camlp4/Camlp4Printers
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Top
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmo


%files devel
%doc LICENSE
%{_bindir}/camlp4*
%{_bindir}/mkcamlp4
%if %{native_compiler}
%{_libdir}/ocaml/camlp4/*.a
%{_libdir}/ocaml/camlp4/*.cmxa
%{_libdir}/ocaml/camlp4/*.cmx
%{_libdir}/ocaml/camlp4/*.o
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.o
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.o
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.o
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Top/*.o
%endif


%changelog
* Tue Aug 20 2019 Richard W.M. Jones <rjones@redhat.com> - 4.08.1-1.git6cb56649
- Update to OCaml 4.08.1.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.08.0-0.gitd32d9973.1.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 4.08.0-0.gitd32d9973.1.5
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.07.0-0.gitd32d9973.1.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.07.0-0.gitd32d9973.1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 4.07.0-0.gitd32d9973.1.2
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 4.07.0-0.gitd32d9973.1.1
- OCaml 4.07.0-rc1 rebuild.

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 4.07.0-0
- OCaml 4.07.0-beta2 rebuild.
- Update to latest upstream version for 4.07 support.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.06.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 4.06.0-1
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-0.4.gitfc12d8c7
- Bump release and rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-0.3.gitfc12d8c7
- Bump release and rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-0.2.gitfc12d8c7
- OCaml 4.05.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-0.1
- Move to upstream 4.05 branch.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.04.2-0.3.gite22d568b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.04.2-0.2.gite22d568b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 4.04.2-0.1.gite22d568b
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 4.04.1-0.4.gite22d568b
- OCaml 4.04.1 rebuild.

* Wed May 10 2017 Richard W.M. Jones <rjones@redhat.com> - 4.04.1-0.3.gite22d568b
- Move along upstream 4.04 branch.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.04.0-0.2.gitc32e8970
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 4.04.0-0.1.gitc32e8970
- Move to upstream 4.04 branch.
- Restore ppc stack limits.

* Wed Aug 31 2016 Dan Horák <dan[at]danny.cz> - 4.02.3-0.4.gitbaf80102
- disable debuginfo subpackage on interpreted builds

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.02.3-0.3.gitbaf80102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.3-0.2.gitbaf80102
- Update to latest 4.02 branch version from git.
- OCaml 4.02.3 rebuild.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.2-0.2.git1e8965ea
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.2-0.1.git1e8965ea
- Move to newest version along 4.02 branch (for ocaml-4.02.2 rebuild).

* Tue Mar 24 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-0.4.gitcf1935d3
- Increase stack limit on ppc64 (RHBZ#1204876).

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-0.3.gitcf1935d3
- Bump release and rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-0.2.gitcf1935d3
- ocaml-4.02.1 rebuild.
- Update to latest upstream git release from branch 4.02.

* Mon Nov 03 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.8.git87c6a6b0
- Bump version and rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.7.git87c6a6b0
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.6.git87c6a6b0
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02.0-0.5.git87c6a6b0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.4.git87c6a6b0
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Sat Jul 19 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.3.git87c6a6b0
- OCaml 4.02.0 beta rebuild.

* Wed Jul 16 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.2
- Initial packaging of new out-of-tree ocaml-camlp4.
