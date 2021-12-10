Name:           mageops-release
Version:        7
Release:        9
Summary:        MageOps RPM repository configuration

Group:          MageOps/Repositories
License:        MIT

Vendor:         creativestyle GmbH <https://creativestyle.de>
URL:            https://github.com/mageops/packages-rpm

Source0:        mageops.repo
Source1:        mageops-2019.pub.asc
Source2:        mageops-2021.pub.asc

BuildArch:      noarch
Requires:       redhat-release >= %{version}
Requires:       epel-release >= %{version}

%description
MageOps RPM repository configuration for CentOS %{version}.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE1} .

%build

%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS-2019
install -Dpm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS-2021
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS-2019
/etc/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS-2021

%changelog
* Fri Dec 10 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 7-9
- Update 2021 key

* Thu Dec 09 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Add 2021 key

* Thu Jun 24 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 7-7
- Add mageops-testing repository that contains packages not ready for use in all environments

* Thu Nov 28 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-5
- Change group to MageOps/Repositories to see what happens
* Wed Nov 27 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-4
- Test bump again
* Wed Nov 27 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-3
- Bump release for testing CI fixes ;)
* Wed Nov 27 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-2
- Who knows?
* Mon Nov 25 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version
