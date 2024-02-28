Name:           amazon-cloudwatch-agent
Version:        1.300032.3
Release:        1%{?dist}
Summary:        Amazon CloudWatch Agent

License:        MIT
URL:            https://github.com/aws/amazon-cloudwatch-agent
Source0:        https://github.com/aws/amazon-cloudwatch-agent/archive/refs/tags/v%{version}.tar.gz

Patch0:         customize-build.patch

BuildRequires:  golang >= 1.13
BuildRequires:  make
BuildRequires:  git
%global debug_package %{nil}


%description
This package provides daemon of Amazon CloudWatch Agent


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1


%build
env
go version
export GOPATH=%{_tmppath}/go
# export GOPROXY="https://goproxy.io,direct"
export GO111MODULE=on

%ifarch x86_64
ARCH=amd64 make amazon-cloudwatch-agent-linux
make package-rpm-amd64
%endif
%ifarch aarch64
ARCH=arm64 make amazon-cloudwatch-agent-linux
make package-rpm-arm64
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
%ifarch x86_64
cp -r ./build/private/linux_amd64/rpm-build/SOURCES/{opt,etc} $RPM_BUILD_ROOT/
%endif
%ifarch aarch64
cp -r ./build/private/linux_arm64/rpm-build/SOURCES/{opt,etc} $RPM_BUILD_ROOT/
%endif
find $RPM_BUILD_ROOT/

############################# create the symbolic links
# bin
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
ln -f -s /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl ${RPM_BUILD_ROOT}/usr/bin/amazon-cloudwatch-agent-ctl
# etc
mkdir -p ${RPM_BUILD_ROOT}/etc/amazon
ln -f -s /opt/aws/amazon-cloudwatch-agent/etc ${RPM_BUILD_ROOT}/etc/amazon/amazon-cloudwatch-agent
# log
mkdir -p ${RPM_BUILD_ROOT}/var/log/amazon
ln -f -s /opt/aws/amazon-cloudwatch-agent/logs ${RPM_BUILD_ROOT}/var/log/amazon/amazon-cloudwatch-agent
# pid
mkdir -p ${RPM_BUILD_ROOT}/var/run/amazon
ln -f -s /opt/aws/amazon-cloudwatch-agent/var ${RPM_BUILD_ROOT}/var/run/amazon/amazon-cloudwatch-agent


%pre
# Stop the agent before upgrades.
if [ $1 -ge 2 ]; then
    if [ -x /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl ]; then
        /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a stop
    fi
fi

%preun
# Stop the agent after uninstall
if [ $1 -eq 0 ] ; then
    if [ -x /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl ]; then
        /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a preun
    fi
fi


%files
%dir /opt/aws/amazon-cloudwatch-agent
%dir /opt/aws/amazon-cloudwatch-agent/bin
%dir /opt/aws/amazon-cloudwatch-agent/doc
%dir /opt/aws/amazon-cloudwatch-agent/etc
%dir /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.d
%dir /opt/aws/amazon-cloudwatch-agent/logs
%dir /opt/aws/amazon-cloudwatch-agent/var
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl
/opt/aws/amazon-cloudwatch-agent/bin/CWAGENT_VERSION
/opt/aws/amazon-cloudwatch-agent/bin/config-translator
/opt/aws/amazon-cloudwatch-agent/bin/config-downloader
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
/opt/aws/amazon-cloudwatch-agent/bin/start-amazon-cloudwatch-agent
/opt/aws/amazon-cloudwatch-agent/doc/amazon-cloudwatch-agent-schema.json
%config(noreplace) /opt/aws/amazon-cloudwatch-agent/etc/common-config.toml
/opt/aws/amazon-cloudwatch-agent/LICENSE
/opt/aws/amazon-cloudwatch-agent/NOTICE

/opt/aws/amazon-cloudwatch-agent/THIRD-PARTY-LICENSES
/opt/aws/amazon-cloudwatch-agent/RELEASE_NOTES
/etc/init/amazon-cloudwatch-agent.conf
/etc/systemd/system/amazon-cloudwatch-agent.service

/usr/bin/amazon-cloudwatch-agent-ctl
/etc/amazon/amazon-cloudwatch-agent
/var/log/amazon/amazon-cloudwatch-agent
/var/run/amazon/amazon-cloudwatch-agent

%changelog
* Thu Jun 24 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.247348.0-2
- rebuilt

* Fri Jun 18 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- Initial release
