Name:           varnish-release
Version:        7
Release:        2
Summary:        Official Varnish Cache RPM repository configuration

Group:          System Environment/Base
License:        MIT

Vendor:         Varnish Cache <https://varnish-cache.org/>
Packager:       creativestyle GmbH <https://creativestyle.pl>
URL:            https://varnish-cache.org/

Source0:        varnish.repo
Source1:        RPM-GPG-KEY-VARNISH60LTS
Source2:        RPM-GPG-KEY-VARNISH60
Source3:        RPM-GPG-KEY-VARNISH61
Source4:        RPM-GPG-KEY-VARNISH62
Source5:        RPM-GPG-KEY-VARNISH63

BuildArch:      noarch
Requires:       redhat-release >= %{version}

%description
Varnish Cache Official RPM repository configuration for CentOS %{version}.

%prep
%setup -q  -c -T

# Script for downloading GPG keys
# for rel in 6{0lts,0,1,2,3} ; do curl -s "https://packagecloud.io/varnishcache/varnish$rel/gpgkey" -o "RPM-GPG-KEY-VARNISH$(echo $rel | awk '{ print toupper($0) }')"; echo "Downloaded GPG key for $rel"; done

%build

%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 "%{SOURCE1}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH60LTS
install -Dpm 644 "%{SOURCE2}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH60
install -Dpm 644 "%{SOURCE3}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH61
install -Dpm 644 "%{SOURCE4}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH62
install -Dpm 644 "%{SOURCE5}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-VARNISH63

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
* Tue Nov 26 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-2
- Fix GPG key download problem by predownloading them
* Tue Nov 26 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version 