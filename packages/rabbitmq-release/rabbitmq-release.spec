Name:           rabbitmq-release
Version:        7
Release:        2
Summary:        Official RabbitMQ RPM repository configuration

Group:          System Environment/Base
License:        MIT

Vendor:         Pivotal Software <https://pivotal.io/>
Packager:       creativestyle GmbH <https://creativestyle.pl>
URL:            https://rabbitmq.org/


# Update GPG keys with
# $ curl -Ls "https://packagecloud.io/rabbitmq/erlang/gpgkey" -o RPM-GPG-KEY-RABBITMQ-ERLANG
# $ curl -Ls "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" -o RPM-GPG-KEY-RABBITMQ-SERVER

Source0:        rabbitmq.repo
Source1:        RPM-GPG-KEY-RABBITMQ-ERLANG
Source2:        RPM-GPG-KEY-RABBITMQ-SERVER

BuildArch:      noarch
Requires:       redhat-release >= %{version}

%description
RabbitMQ/Erlang Official RPM repository configuration for CentOS %{version}.

%prep
%setup -q  -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 "%{SOURCE1}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-RABBITMQ-ERLANG
install -Dpm 644 "%{SOURCE2}" $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-RABBITMQ-SERVER

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-RABBITMQ-*

%changelog
* Thu Feb 22 2024 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 7-2
- rebuilt

* Tue Nov 26 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 7-1
- Initial version 