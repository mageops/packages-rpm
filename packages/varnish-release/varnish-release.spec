Name:           varnish-release
Version:        7
Release:        2
Summary:        Official Varnish Cache RPM repository configuration

Group:          System Environment/Base
License:        MIT

Vendor:         Varnish Cache <https://varnish-cache.org/>
Packager:       creativestyle GmbH <https://creativestyle.pl>
URL:            https://varnish-cache.org/

# Get final key filenames like this
# $ for url in https://packagecloud.io/varnishcache/varnish6{0lts,0,1,2,3}/gpgkey ; do echo -e "$url ->\n\t$(curl -Ls -o /dev/null -w %{url_effective} "$url")"; done

Source0:        varnish.repo
Source1:        https://d28dx6y1hfq314.cloudfront.net/3228/8576/gpg/varnishcache-varnish60lts-3AEAFFBB82FBBA5F.pub.gpg?t=1574787847_0fd48a1eb4f20147f2e224e5e0a87cd7f7d2fcce
Source2:        https://d28dx6y1hfq314.cloudfront.net/3228/7343/gpg/varnishcache-varnish60-47954A833C3E7225.pub.gpg?t=1574787848_cfb7e39c4826ad9d906ac080d59748467b7b1237
Source3:        https://d28dx6y1hfq314.cloudfront.net/3228/8620/gpg/varnishcache-varnish61-7DF4C6DB50D87781.pub.gpg?t=1574787849_4af56ef5111e637e966e78065876af09a4c92f7e
Source4:        https://d28dx6y1hfq314.cloudfront.net/3228/9910/gpg/varnishcache-varnish62-0D42823DD1135F8E.pub.gpg?t=1574787850_7f6b960008a3a507e97325106320a2a719b814d0
Source5:        https://d28dx6y1hfq314.cloudfront.net/3228/11237/gpg/varnishcache-varnish63-EB01D0ACA3C53736.pub.gpg?t=1574787851_5d060a2b28dbea2435561da2d6aa743a681108c6

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