%global binary      aws
%global pkg         awscli
%global venv_path   %{pkg}

# disable automatic compilation and od this manually
%global _python_bytecompile_extra 0
%global _python_bytecompile_errors_terminate_build 0
%undefine __brp_python_bytecompile

Name:           %{pkg}
Version:        1.16.284
Release:        1%{?dist}

Group:          System Environment/Libraries
Summary:        Universal Command Line Environment for AWS
License:        Apache License 2.0

Vendor:         Amazon.com
Packager:       creativestyle GmbH <https://creativestyle.de>
URL:            http://aws.amazon.com/cli/

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-virtualenv
BuildRequires:  python%{python3_pkgversion}-docutils

Requires:       python%{python3_pkgversion} >= 3.6
Requires:       groff

%description
This package provides a unified command line interface to Amazon Web Services.

%prep

%build
%{__python3} -m virtualenv --no-site-packages -p %{__python3} empty_env
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
mkdir -p %{buildroot}%{_libdir}
cp -r %{venv_path} %{buildroot}%{_libdir}/%{pkg}

# force compilation with python3
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/%{pkg}

%posttrans
alternatives --install %{_bindir}/%{binary} %{binary} %{_libdir}/%{pkg}/bin/%{binary} 1
ln -s %{_bindir}/python %{_libdir}/%{pkg}/bin/python
ln -s %{_bindir}/python3 %{_libdir}/%{pkg}/bin/python3

%files
%ghost %{_bindir}/%{binary}
%ghost %{_libdir}/%{pkg}/bin/python
%ghost %{_libdir}/%{pkg}/bin/python3
%{_libdir}/%{pkg}/

%changelog
* Tue Nov 19 2019 Filip Sobalski <filip.sobalski@creativestyle.pl> - 1.16.284
- Bump version
- Cleanup and simply the specfile
- Switch %_datadir to %_libdir installation

* Fri Oct 11 2019 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.16.257-1
- new version

* Mon Oct 07 2019 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 1.16.253-1
- Initial package.
