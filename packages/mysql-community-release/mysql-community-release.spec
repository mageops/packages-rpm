Name:           mysql-community-release
Version:        el7
Release:        8
Summary:        mysql-community-release - MySQL repository configuration for yum

Group:          System Environment/Base
License:        GPLv2
URL:            http://dev.mysql.com
Source0:        mysql-community.repo
Source1:        mysql-community-source.repo
Source2:        RPM-GPG-KEY-mysql
Source3:        RPM-GPG-KEY-mysql-2022
Source4:        mysql-community-debuginfo.repo
Source5:        RPM-GPG-KEY-mysql-2023

BuildArch:      noarch
Conflicts:      mysql57-community-release

%description
Package for installation of setup/configuration files required for
installation of MySQL packages by yum.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 "%{SOURCE2}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-mysql
install -Dpm 644 "%{SOURCE3}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-mysql-2022
install -Dpm 644 "%{SOURCE5}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-mysql-2023
install -Dpm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/mysql-community.repo
install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/mysql-community-source.repo
install -Dpm 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/mysql-community-debuginfo.repo

%files
%defattr(-,root,root,-)
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-mysql
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-mysql-2022
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-mysql-2023
%config(noreplace) %{_sysconfdir}/yum.repos.d/*

%changelog
* Wed Apr 17 2024 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - el7-8
- Update repositories

* Wed Mar 22 2023 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - el7-7
- Update packages

* Fri Jun 18 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Initial release
