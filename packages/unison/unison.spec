Name:             unison
Version:          2.52.0
Release:          1%{?dist}

Summary:          Multi-master File synchronization tool (text UI)

Group:            Applications/File
License:          GPLv3+

Vendor:           Benjamin Pierce
URL:              https://www.cis.upenn.edu/~bcpierce/unison

Source0:          https://github.com/bcpierce00/unison/archive/v%{version}.tar.gz

BuildRequires:    ocaml
BuildRequires:    make
BuildRequires:    ctags-etags
BuildRequires:    which

%description
Unison is a file-synchronization tool for OSX, Unix, and Windows.

It allows two replicas of a collection of files and directories to be stored
on different hosts (or different disks on the same host), modified separately,
and then brought up to date by propagating the changes in each replica
to the other.

/ Original author's description via %{URL}

%prep
%setup -q -n unison-%{version}

%build
# Do not use parallel build (-j flag) as it won't produce binaries without error
%{__make} UISTYLE=text NATIVE=true STATIC=false DEBUGGING=false

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 src/unison %{buildroot}%{_bindir}/unison
install -p -m 755 src/unison-fsmonitor %{buildroot}%{_bindir}/unison-fsmonitor

%files
%defattr(-,root,root,-)
%{_bindir}/unison
%{_bindir}/unison-fsmonitor

%changelog
* Wed Mar 30 2022 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 2.52.0-1
- new version

* Fri May 15 2020 Filip Sobalski <filip.sobalski@creativestyle.pl> - 2.51.2-1
- Initial version
