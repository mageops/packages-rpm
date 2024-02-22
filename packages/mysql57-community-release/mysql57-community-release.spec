Name:           mysql57-community-release
Version:        el7
Release:        11
Summary:        mysql-community-release - MySQL repository configuration for yum

Group:          System Environment/Base
License:        GPLv2
URL:            http://dev.mysql.com
Source0:        mysql-community.repo
Source1:        mysql-community-source.repo
Source2:        RPM-GPG-KEY-mysql

BuildArch:      noarch
Conflicts:      mysql-community-release

%description
Package for installation of setup/configuration files required for
installation of MySQL packages by yum.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-mysql
install -Dpm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/mysql-community.repo
install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/mysql-community-source.repo

%files
%defattr(-,root,root,-)
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-mysql
%config(noreplace) %{_sysconfdir}/yum.repos.d/*

%changelog
* Thu Feb 22 2024 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - el7-11
- rebuilt

* Fri Jun 18 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Initial release
