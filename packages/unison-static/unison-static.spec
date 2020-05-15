Name:             unison-static
Version:          2.51.2
Release:          1%{?dist}

Summary:          Multi-master File synchronization tool (static binary; text UI)

Group:            Applications/File
License:          GPLv3+

Vendor:           Benjamin Pierce
Packager:         creativestyle GmbH <https://creativestyle.de>
URL:              https://www.cis.upenn.edu/~bcpierce/unison

Source0:          unison
Source1:          unison-fsmonitor

%description
Unison is a file-synchronization tool for OSX, Unix, and Windows.

It allows two replicas of a collection of files and directories to be stored
on different hosts (or different disks on the same host), modified separately,
and then brought up to date by propagating the changes in each replica
to the other.

/ Original author's description via %{URL}

%prep


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0} %{buildroot}%{_bindir}/unison
install -p -m 755 %{SOURCE1} %{buildroot}%{_bindir}/unison-fsmonitor

%files
%defattr(-,root,root,-)
%{_bindir}/unison
%{_bindir}/unison-fsmonitor

%changelog
* Fri May 15 2020 Filip Sobalski <filip.sobalski@creativestyle.pl> - 2.51.2-1
- Initial version
