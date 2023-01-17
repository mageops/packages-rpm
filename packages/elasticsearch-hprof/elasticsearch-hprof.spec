%global crate elasticsearch-hprof
%global git_sha 1981363b063396d24ce1f8645e4089e52e508b58
%global debug_package %{nil}

Name:           rust-%{crate}
Version:        0.2.0
Release:        1%{?dist}
Summary:        Elasticsearch hprof memory dump reader

# Upstream license specification: MIT
License:        MIT
URL:            https://github.com/Szpadel/elasticsearch-hprof
Source:         https://github.com/Szpadel/elasticsearch-hprof/archive/%{git_sha}.tar.gz
Source1:        elasticsearch-crash-handler.service
Source2:        elasticsearch-crash-handler.path

%ifnarch aarch64
BuildRequires:   cargo
BuildRequires:   rust >= 1.52
%endif

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
%ifarch aarch64
# aarch64 do not have recent rust available, therefore we install it manually here
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain 1.52-aarch64-unknown-linux-gnu
%endif

%build
%ifarch aarch64
source $HOME/.cargo/env
%endif
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
