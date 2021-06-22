Name:           remi-release
Version:        7.9
Release:        1%{?dist}
Summary:        YUM configuration for remi repository

License:        CC-BY-SA
URL:            https://remirepo.net
Source0:        remi-release.tar.gz
Vendor:         Remi's RPM repository <https://rpms.remirepo.net/>
BuildArch:      noarch

%description
This package contains yum configuration for the Remi's RPM Repository,
as well as the public GPG keys used to sign them.

Only the "remi-safe" repository is enabled after installation.

For proper PHP installation, see https://rpms.remirepo.net/wizard/

FAQ:     https://blog.remirepo.net/pages/English-FAQ
Forum:   https://forum.remirepo.net/
Twitter: https://twitter.com/RemiRepository

%prep
%setup -q -n remi-release

%build


%install
rm -rf $RPM_BUILD_ROOT
for file in etc/pki/rpm-gpg/*;do
    install -Dpm 644 "$file" "$RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/$(basename "$file")"
done
for file in etc/yum.repos.d/*;do
    install -Dpm 644 "$file" "$RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/$(basename "$file")"
done


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog
* Fri Jun 18 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
-
