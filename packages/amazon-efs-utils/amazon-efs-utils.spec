Name:             amazon-efs-utils
Version:          1.14
Release:          2%{?dist}

Group:            Amazon/Tools
Summary:          This package provides utilities for simplifying the use of EFS file systems
License:          MIT

Vendor:           Amazon.com
Packager:         creativestyle GmbH <https://creativestyle.de>
URL:              https://aws.amazon.com/efs

Source:           https://github.com/aws/efs-utils/archive/v%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    systemd

Requires:         nfs-utils
Requires:         systemd
Requires:         openssl >= 1.0.2
Requires:         stunnel >= 4.56
Requires:         python >= 2.7

%description
This package provides utilities for simplifying the use of EFS file systems

%define pkgdirname efs-utils-%{version}

%prep
%setup -n %{pkgdirname}

%install
mkdir -p %{buildroot}%{_sysconfdir}/amazon/efs
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{_builddir}/%{pkgdirname}/dist/amazon-efs-mount-watchdog.service %{buildroot}%{_unitdir}

mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_localstatedir}/log/amazon/efs
mkdir -p  %{buildroot}%{_mandir}/man8

install -p -m 644 %{_builddir}/%{pkgdirname}/dist/efs-utils.conf %{buildroot}%{_sysconfdir}/amazon/efs
install -p -m 444 %{_builddir}/%{pkgdirname}/dist/efs-utils.crt %{buildroot}%{_sysconfdir}/amazon/efs
install -p -m 755 %{_builddir}/%{pkgdirname}/src/mount_efs/__init__.py %{buildroot}/sbin/mount.efs
install -p -m 755 %{_builddir}/%{pkgdirname}/src/watchdog/__init__.py %{buildroot}%{_bindir}/amazon-efs-mount-watchdog
install -p -m 644 %{_builddir}/%{pkgdirname}/man/mount.efs.8 %{buildroot}%{_mandir}/man8

%files
%defattr(-,root,root,-)
%{_unitdir}/amazon-efs-mount-watchdog.service
%{_sysconfdir}/amazon/efs/efs-utils.crt
/sbin/mount.efs
%{_bindir}/amazon-efs-mount-watchdog
/var/log/amazon
%{_mandir}/man8/mount.efs.8.gz

%config(noreplace) %{_sysconfdir}/amazon/efs/efs-utils.conf

%post
%systemd_post amazon-efs-mount-watchdog.service

%preun
%systemd_preun amazon-efs-mount-watchdog.service

%postun
%systemd_postun_with_restart amazon-efs-mount-watchdog.service

%clean

%changelog
* Thu Feb 22 2024 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.14-2
- rebuilt

* Tue Nov 19 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 1.14
- Bump version 
