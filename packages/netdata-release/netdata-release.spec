Name:           netdata-release
Version:        7
Release:        1
Summary:        Netdata Packagecloud RPM repo config

License:        MIT

Vendor:         Netdata <https://netdata.cloud/>
URL:            https://www.netdata.cloud/


# Update GPG keys with
# $ curl -Ls "https://packagecloud.io/netdata/netdata/gpgkey" -o RPM-GPG-KEY-NETDATA

Source0:        netdata.repo
Source1:        RPM-GPG-KEY-NETDATA

BuildArch:      noarch
Requires:       redhat-release >= %{version}

%description
Netdata Official PackageCloud RPM repository configuration for CentOS %{version}.

%prep
%setup -q  -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 "%{SOURCE1}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-NETDATA

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-NETDATA

%changelog
* Mon Jan 20 2020 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version
