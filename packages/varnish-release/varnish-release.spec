Name:           varnish-release
Version:        7
Release:        1
Summary:        Official Varnish Cache RPM repository configuration

Group:          System Environment/Base
License:        MIT

Vendor:         Varnish Cache <https://varnish-cache.org/>
Packager:       creativestyle GmbH <https://creativestyle.pl>
URL:            https://varnish-cache.org/

Source0:        varnish.repo
Source1:        https://packagecloud.io/varnishcache/varnish60lts/gpgkey
Source2:        https://packagecloud.io/varnishcache/varnish60/gpgkey
Source3:        https://packagecloud.io/varnishcache/varnish61/gpgkey
Source4:        https://packagecloud.io/varnishcache/varnish62/gpgkey
Source5:        https://packagecloud.io/varnishcache/varnish63/gpgkey

BuildArch:      noarch
Requires:       redhat-release >= %{version}

%description
Varnish Cache Official RPM repository configuration for CentOS %{version}.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE1} .
install -pm 644 %{SOURCE2} .
install -pm 644 %{SOURCE3} .
install -pm 644 %{SOURCE4} .
install -pm 644 %{SOURCE5} .

%build

%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH60LTS
install -Dpm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH60
install -Dpm 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH61
install -Dpm 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH62
install -Dpm 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH63

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-VARNISH*

%changelog
* Tue Nov 26 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version 