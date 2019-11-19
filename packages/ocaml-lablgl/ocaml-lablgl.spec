%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-lablgl
Epoch:          1
Version:        1.06
Release:        1%{?dist}
Summary:        LablGL is an OpenGL interface for Objective Caml
License:        BSD

URL:            http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgl.html
Source0:        https://github.com/garrigue/lablgl/archive/v1.06/%{name}-%{version}.tar.gz

BuildRequires:  freeglut-devel 
BuildRequires:  ocaml >= 3.12.1-3
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:	ocaml-labltk-devel


%description
LablGL is is an Objective Caml interface to OpenGL. Support is
included for use inside LablTk, and LablGTK also includes specific
support for LablGL.  It can be used either with proprietary OpenGL
implementations (SGI, Digital Unix, Solaris...), with XFree86 GLX
extension, or with open-source Mesa.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       ocaml-labltk-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n lablgl-%{version}

cat > Makefile.config <<EOF
%if %{opt}
CAMLC = ocamlc.opt
CAMLOPT = ocamlopt.opt -g
%else
CAMLC = ocamlc
CAMLOPT = ocamlc -g
%endif
BINDIR = %{_bindir}
XINCLUDES = -I%{_prefix}/X11R6/include
XLIBS = -lXext -lXmu -lX11
TKINCLUDES = -I%{_includedir}
GLINCLUDES =
GLLIBS = -lGL -lGLU
GLUTLIBS = -lglut -lXxf86vm
RANLIB = :
LIBDIR = %{_libdir}/ocaml
DLLDIR = %{_libdir}/ocaml/stublibs
INSTALLDIR = %{_libdir}/ocaml/lablGL
TOGLDIR=Togl
COPTS = $RPM_OPT_FLAGS
EOF


%build
# Parallel builds don't work.
unset MAKEFLAGS
make all \
%if %{opt}
opt
%endif


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/lablGL
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
make INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/lablGL \
    DLLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs \
    BINDIR=$RPM_BUILD_ROOT%{_bindir} \
    install

# Make and install a META file.
cat <<EOM >META
version="%{version}"
directory="+lablgl"
archive(byte) = "lablgl.cma"
archive(native) = "lablgl.cmxa"

package "togl" (
  requires = "labltk lablgl"
  archive(byte) = "togl.cma"
  archive(native) = "togl.cmxa"
)

package "glut" (
  requires = "lablgl"
  archive(byte) = "lablglut.cma"
  archive(native) = "lablglut.cmxa"
)
EOM
cp META $RPM_BUILD_ROOT%{_libdir}/ocaml/lablGL

# Remove unnecessary *.ml files (ones which have a *.mli).
pushd $RPM_BUILD_ROOT%{_libdir}/ocaml/lablGL
for f in *.ml; do \
  b=`basename $f .ml`; \
  if [ -f "$b.mli" ]; then \
    rm $f; \
  fi; \
done
popd


%files
%doc README
%dir %{_libdir}/ocaml/lablGL
%{_libdir}/ocaml/lablGL/*.cma
%{_libdir}/ocaml/lablGL/*.cmi
%{_libdir}/ocaml/stublibs/*.so
%{_bindir}/lablgl
%{_bindir}/lablglut


%files devel
%doc CHANGES COPYRIGHT README LablGlut/examples Togl/examples
%{_libdir}/ocaml/lablGL/META
%{_libdir}/ocaml/lablGL/*.a
%if %{opt}
%{_libdir}/ocaml/lablGL/*.cmxa
%{_libdir}/ocaml/lablGL/*.cmx
%endif
%{_libdir}/ocaml/lablGL/*.mli
%{_libdir}/ocaml/lablGL/build.ml


%changelog
* Sat Aug 10 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.06-1
- New upstream version 1.06.
- This removes the camlp4 dependency (RHBZ#1736347).
- Fix for new source URL.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.05-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.05-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.05-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-30
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-29
- OCaml 4.07.0-rc1 rebuild.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.05-28
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.05-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-26
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-25
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.05-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.05-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-22
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-21
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.05-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-19
- Rebuild for OCaml 4.04.0.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.05-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-17
- OCaml 4.02.3 rebuild.

* Wed Jul 22 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-16
- Fix bytecode builds (patch supplied by Rafael Fonseca).

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-15
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-14
- ocaml-4.02.2 rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-13
- Bump release and rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-12
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-11
- Bump release and rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-10
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-9
- Bump release and rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-8
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-6
- Bump release and rebuild.

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-5
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.05-4
- OCaml 4.02.0 beta rebuild.

* Thu Jun 19 2014 Richard W.M. Jones <rjones@redhat.com> - 1.05-3
- Make -devel subpackage depend on the epoch + base version.

* Wed Jun 18 2014 Richard W.M. Jones <rjones@redhat.com> - 1.05-1
- New upstream version 1.05.
- Requires Epoch because upstream version went from 20120306->1.05.
- Fixes FTBFS (RHBZ#1106619).
- Use ExclusiveArch and add a comment about how we could fix this.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120306-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 20120306-7
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120306-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120306-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Orion Poplawski <orion@cora.nwra.com> - 20120306-4
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120306-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 20120306-2
- Rebuild for OCaml 4.00.0.

* Fri Jun 8 2012 Orion Poplawski <orion@cora.nwra.com> - 20120306-1
- Update to version 20120306.
- Update URL.
- Build for OCaml 4.00.0.

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.04-7
- Bump and rebuild against new OCaml compiler in ARM.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.04-6
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 1.04-4
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.04-3
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.04-1
- Rebuild for OCaml 3.11.1.
- New upstream version 1.04.
- Patch for Tk 8.5 is now upstream.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-6
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-5
- Rebuild for OCaml 3.11.0

* Wed May 14 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-4
- Remove BRs for camlp4, labltk.
- Remove old Provides.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-3
- Rebuild for OCaml 3.10.2.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-2
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-1
- New upstream version 1.03.
- Fix for Tk 8.5.
- Rebuild for OCaml 3.10.1.

* Fri Sep  7 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.02-15
- Rebuild

* Thu Aug 30 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.02-13
- Rebuild

* Sat Jul  7 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.02-12
- exclude arch ppc64

* Sat Jul  7 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.02-11
- added buildreq ocaml-camlp4-devel

* Fri Jul  6 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.02-10
- renamed package from lablgl to ocaml-lablgl

* Sat Dec  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.02-9
- Rebuild for ocaml 3.09.3

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.02-8
- Rebuild for FE6

* Wed May 10 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.02-7
- rebuilt for ocaml 3.09.2

* Sun Feb 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.02-4
- Rebuild for ocaml 3.09.1

* Sat Feb 25 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.02-3
- Rebuild for Fedora Extras 5

* Tue Nov  1 2005 Gerard Milmeister <gemi@bluewin.ch> - 1.02-2
- build opt libraries

* Tue Nov  1 2005 Gerard Milmeister <gemi@bluewin.ch> - 1.02-1
- New Version 1.02

* Sun Sep 11 2005 Gerard Milmeister <gemi@bluewin.ch> - 1.01-7
- Rebuild with new ocaml

* Thu May 26 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 1.01-6
- Bump and rebuild with new ocaml.
  
* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.01-5
- rebuild on all arches

* Fri Apr  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Apr  1 2005 Gerard Milmeister <gemi@bluewin.ch> - 1.01-3
- Rebuild for ocaml 3.08.3

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:1.01-2
- Removed %%{_smp_mflags} as it breaks the build

* Thu Aug 19 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:1.01-0.fdr.1
- New Version 1.01

* Mon Dec  1 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:1.00-0.fdr.4
- Patch to used GL/freeglut.h instead of GL/glut.h
- Add BuildRequires for labltk

* Fri Nov 28 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:1.00-0.fdr.3
- Add BuildRequires for camlp4
