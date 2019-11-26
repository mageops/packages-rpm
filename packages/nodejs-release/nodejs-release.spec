Name:           nodejs-release
Version:        7
Release:        1
Summary:        Official NodeJS RPM repository configuration

Group:          System Environment/Base
License:        MIT

Vendor:         NodeJS Foundation <https://nodejs.org/>
Packager:       creativestyle GmbH <https://creativestyle.pl>
URL:            https://nodejs.org/

Source0:        nodejs.repo
Source1:        https://rpm.nodesource.com/pub/el/NODESOURCE-GPG-SIGNING-KEY-EL

BuildArch:      noarch
Requires:       redhat-release >= %{version}

%description
NodeJS Nodesource RPM repository configuration for CentOS %{version}.
See https://github.com/nodesource/distributions for more information.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE1} .

%build

%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 "%{SOURCE1}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/NODESOURCE-GPG-SIGNING-KEY-EL

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/NODESOURCE-GPG-SIGNING-KEY-EL

%changelog
* Tue Nov 26 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version 