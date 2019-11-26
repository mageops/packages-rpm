Name:           nginx-release
Version:        7
Release:        1
Summary:        Official nginx HTTP Server RPM repository configuration

Group:          System Environment/Base
License:        MIT

Vendor:         nginx HTTP Server <https://nginx.org/>
Packager:       creativestyle GmbH <https://creativestyle.pl>
URL:            https://nginx.org/

Source0:        nginx.repo
Source1:        https://nginx.org/keys/nginx_signing.key

BuildArch:      noarch
Requires:       redhat-release >= %{version}

%description
nginx HTTP Server Official RPM repository configuration for CentOS %{version}.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE1} .

%build

%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 "%{SOURCE1}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-NGINX

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-NGINX

%changelog
* Tue Nov 26 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version 