%define tinyproxy_confdir %{_sysconfdir}/tinyproxy
%define tinyproxy_datadir %{_datadir}/tinyproxy
%define tinyproxy_rundir  %{_localstatedir}/run/tinyproxy
%define tinyproxy_logdir  %{_localstatedir}/log/tinyproxy
%define tinyproxy_user    tinyproxy
%define tinyproxy_group   tinyproxy

Name:           tinyproxy
Version:        1.11.1
Release:        1%{?dist}
Summary:        A small, efficient HTTP/SSL proxy daemon

License:        GPLv2+
URL:            https://github.com/tinyproxy/

Source0:        https://github.com/tinyproxy/tinyproxy/releases/download/%{version}/%{name}-%{version}.tar.xz
Source1:        %{name}.service
Source2:        %{name}.logrotate
Source3:        %{name}.tmpfiles

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  asciidoc
%if 0%{?rhel} < 8
BuildRequires: systemd
%else
BuildRequires: systemd-rpm-macros
%{?systemd_requires}
%endif


%description
tinyproxy is a small, efficient HTTP/SSL proxy daemon that is very useful in a
small network setting, where a larger proxy like Squid would either be too
resource intensive, or a security risk.


%prep
%autosetup -p 1


%build
%configure --sysconfdir=%{_sysconfdir} \
    --enable-reverse \
    --enable-transparent

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/%{name}.conf
%{__install} -p -d -m 0700 %{buildroot}%{_localstatedir}/run/%{name}
%{__install} -p -d -m 0700 %{buildroot}%{_localstatedir}/log/%{name}


%pre
if [ $1 == 1 ]; then
    %{_sbindir}/useradd -c "tinyproxy user" -s /bin/false -r -d %{tinyproxy_rundir} %{tinyproxy_user} 2>/dev/null || :
fi


%post
%if 0%{?rhel} < 8
/bin/systemctl --system daemon-reload &> /dev/null || :
/bin/systemctl --system enable %{name}.service &> /dev/null || :
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
%systemd_post %{name}.service
%endif


%preun
%if 0%{?fedora} || 0%{?rhel} >= 8
%systemd_preun %{name}.service
%endif

%postun
%if 0%{?rhel} < 8
/bin/systemctl --system daemon-reload &> /dev/null || :
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
%systemd_postun_with_restart %{name}.service
%endif

%files
%doc AUTHORS COPYING README NEWS docs/*.txt README.md
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man5/%{name}.conf.5.gz
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{tinyproxy_datadir}
%dir %{tinyproxy_confdir}
%config(noreplace) %{tinyproxy_confdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,%{tinyproxy_user},%{tinyproxy_group}) %dir %{tinyproxy_rundir}
%attr(-,%{tinyproxy_user},%{tinyproxy_group}) %dir %{tinyproxy_logdir}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/NEWS
%{_docdir}/%{name}/README
%{_docdir}/%{name}/README.md


%changelog
* Tue Jul 04 2023 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.11.1-1
- new version

* Wed May 03 2023 Carl George <carl@george.computer> - 1.8.4-2
- Backport fix for CVE-2017-11747

* Tue Mar 07 2017 Michael Adam <obnox@samba.org> - 1.8.4-1
- Update to new upstream version 1.8.4

* Wed Jul 29 2015 Arnaud Begot <arnaud.begot@worldline.com> - 1.8.3-2
- initial version for rhel/CentOS 7

* Mon Sep 09 2013 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.8.3-1
- update to upstream 1.8.3

* Sat Jun 05 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.8.2-1
- update to upstream 1.8.2

* Tue Apr 06 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.8.1-1
- update to upstream 1.8.1

* Wed Feb 17 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.8.0-1
- update to upstream 1.8.0
- add logrotate configuration

* Sun Oct 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.5-1
- update to upstream 1.6.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.4-3
- add --enable-transparent-proxy option (#466808)

* Sun Aug 24 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.4-2
- update to upstream 1.6.4 final

* Sun Jun 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.4-1
- update to upstream candidate 1.6.4

* Wed Apr 16 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.3-2
- fix spec review issues
- fix initscript

* Sun Mar 09 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.3-1
- Initial rpm configuration
