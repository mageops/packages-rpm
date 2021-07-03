%global crate elasticsearch-hprof
%global git_sha 9e79d6d924a18d7de28f9eb881806dfc267f5459
Name:           rust-%{crate}
Version:        0.1.0
Release:        2%{?dist}
Summary:        Elasticsearch hprof memory dump reader

# Upstream license specification: MIT
License:        MIT
URL:            https://github.com/Szpadel/elasticsearch-hprof
Source:         https://github.com/Szpadel/elasticsearch-hprof/archive/%{git_sha}.tar.gz
Source1:        elasticsearch-crash-handler.service
Source2:        elasticsearch-crash-handler.path

BuildRequires:   cargo
BuildRequires:   rust >= 1.52

ExclusiveArch:  x86_64 i386 i486 i586 i686 pentium3 pentium4 athlon geode armv7hl aarch64 ppc64 ppc64le riscv64 s390x

%global _description %{expand:
Elasticsearch hprof memory dump reader.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}

%description -n %{crate} %{_description}

%files       -n %{crate}
%{_bindir}/elasticsearch-hprof
%{_unitdir}/elasticsearch-crash-handler.path
%{_unitdir}/elasticsearch-crash-handler.service

%prep
%autosetup -n %{crate}-%{git_sha} -p1

%build
cargo build --release

%post
%systemd_post elasticsearch-crash-handler.path

%preun
%systemd_preun elasticsearch-crash-handler.path

%postun
%systemd_postun_with_restart elasticsearch-crash-handler.path

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 target/release/elasticsearch-hprof %{buildroot}%{_bindir}/elasticsearch-hprof
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/elasticsearch-crash-handler.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/elasticsearch-crash-handler.path


%changelog
* Sat Jul 03 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 0.1.0-2
- Fix typo in systemd service

* Tue Jun 01 2021 Piotr Rogowski <piotrekrogowski@gmail.com> - 0.1.0-1
- Initial package
