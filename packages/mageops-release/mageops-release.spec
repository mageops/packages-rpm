Name:           mageops-release
Version:        7
Release:        2
Summary:        MageOps RPM repository configuration

Group:          System Environment/Base
License:        MIT

Vendor:         creativestyle GmbH <https://creativestyle.de>
Packager:       creativestyle GmbH <https://creativestyle.de>
URL:            https://github.com/mageops/rpm

Source0:        mageops.repo
Source1:        https://raw.githubusercontent.com/mageops/rpm/master/rpm-gpg-key.pub.asc

BuildArch:      noarch
Requires:       redhat-release >= %{version}

%description
MageOps RPM repository configuration for CentOS %{version}.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE1} .

%build

%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-MAGEOPS

%changelog
* Mon Nov 25 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version 