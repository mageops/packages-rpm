Name:             aws-excfwd
Version:          1.0.1
Release:          2%{?dist}

Group:            Amazon/Tools
Summary:          Provides command that forwards new files to CloudWatch Logs
License:          MIT

Vendor:           creativestyle Polska <https://creativestyle.pl>
Packager:         creativestyle Polska <https://creativestyle.pl>
URL:              https://github.com/mageops/php-report-cloudwatch-forwarder

Source0:          https://github.com/mageops/php-report-cloudwatch-forwarder/releases/download/%{version}/aws-excfwd

BuildArch:        noarch

Requires:         php-cli >= 7.1

%description
Forwards exception reports stored as individual files to AWS CloudWatch Logs


%prep
%setup -q  -c -T

%install
mkdir -p %{buildroot}%{_bindir}

install -p -m 755 %{SOURCE0} %{buildroot}%{_bindir}/aws-excfwd

%files
%defattr(-,root,root,-)
%{_bindir}/aws-excfwd

%changelog
* Thu Feb 22 2024 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.0.1-2
- rebuilt

* Tue Nov 26 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 1.0.1
- Initial version

