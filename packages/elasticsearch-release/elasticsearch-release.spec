Name:           elasticsearch-release
Version:        7
Release:        2
Summary:        Official Elasticsearch RPM repository configuration

Group:          System Environment/Base
License:        MIT

Vendor:         Elasticsearch B.V. <https://elastic.co/>
Packager:       creativestyle GmbH <https://creativestyle.pl>
URL:            https://elastic.co/

Source0:        elasticsearch.repo
Source1:        https://artifacts.elastic.co/GPG-KEY-elasticsearch

BuildArch:      noarch

%description
Elasticsearch Official RPM repository configuration for CentOS %{version}.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE1} .

%build

%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 "%{SOURCE1}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ELASTICSEARCH

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-ELASTICSEARCH

%changelog
* Mon Dec 09 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-2
- Fix GPG key path
* Tue Nov 26 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version 
