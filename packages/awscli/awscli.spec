%global pkg awscli
%global binary aws
%global venv_path %{pkg}

Name:           %{pkg}
Version:        1.16.257
Release:        1%{?dist}
Summary:        Universal Command Line Environment for AWS

License:        Apache License 2.0
URL:            http://aws.amazon.com/cli/
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-virtualenv
Requires:       python%{python3_pkgversion}

%description
aws-cli This package provides a unified command line interface to Amazon Web
Services.The aws-cli package works on Python versions:* 2.6.5 and greater *
2.7.x and greater * 3.3.x and greater * 3.4.x and greater * 3.5.x and greater *
3.6.x and greater * 3.7.x and greater.. attention:: We recommend that all
customers regularly monitor the Amazon Web Services Security Bulletins website_
for any...

%prep

%build
%{__python3} -m virtualenv -p %{__python3} empty_env
mkdir -p %{venv_path}
%{__python3} -m venv --copies %{venv_path}
cp empty_env/bin/activate_this.py %{venv_path}/bin/
source %{venv_path}/bin/activate
pip install %{pkg}==%{version}
pip uninstall -y pip setuptools
%{__python3} -m virtualenv --relocatable %{venv_path}
deactivate
rm -f %{venv_path}/bin/{activate,activate.csh,activate.fish,Activate.ps1,activate.bat}
rm %{venv_path}/bin/python %{venv_path}/bin/python3

%install
mkdir -p %{buildroot}%{_datadir}
cp -r %{venv_path} %{buildroot}%{_datadir}/%{pkg}

%posttrans
alternatives --install %{_bindir}/%{binary} %{binary} %{_datadir}/%{pkg}/bin/%{binary} 1
ln -s %{_bindir}/python %{_datadir}/%{pkg}/bin/python
ln -s %{_bindir}/python3 %{_datadir}/%{pkg}/bin/python3

%files
%ghost %{_bindir}/%{binary}
%ghost %{_datadir}/%{pkg}/bin/python
%ghost %{_datadir}/%{pkg}/bin/python3
%{_datadir}/%{pkg}/

%changelog
* Fri Oct 11 2019 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.16.257-1
- new version

* Mon Oct 07 2019 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.16.253-1
- Initial package.
