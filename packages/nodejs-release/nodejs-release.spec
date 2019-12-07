Name:           nodejs-release
Version:        7
Release:        2
Summary:        Nodesource and Yarnpkg RPM Repos coveniently bundled

Group:          System Environment/Base
License:        MIT

Vendor:         NodeJS Foundation <https://nodejs.org/>
Packager:       creativestyle GmbH <https://creativestyle.pl>
URL:            https://nodejs.org/

Source0:        nodejs.repo
Source1:        https://rpm.nodesource.com/pub/el/NODESOURCE-GPG-SIGNING-KEY-EL
Source2:        https://dl.yarnpkg.com/rpm/pubkey.gpg

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

install -Dpm 644 "%{SOURCE1}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/NODE-GPG-SIGNING-KEY-EL
install -Dpm 644 "%{SOURCE2}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/YARNPKG-GPG-SIGNING-KEY-EL

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
* Sat Dev 07 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-2
- Add yarn repo
* Tue Nov 26 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version