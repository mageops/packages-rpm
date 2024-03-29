%global crate elasticsearch-hprof
%global git_sha 4628161ec74e072804df65833692a143d3bbc59b
%global debug_package %{nil}

# Select rust toolchain
%ifarch aarch64
%global rust_toolchain 1.75-aarch64-unknown-linux-gnu
%endif
%ifarch x86_64
%global rust_toolchain 1.75-x86_64-unknown-linux-gnu
%endif

Name:           rust-%{crate}
Version:        0.2.1
Release:        1%{?dist}
Summary:        Elasticsearch hprof memory dump reader

# Upstream license specification: MIT
License:        MIT
URL:            https://github.com/Szpadel/elasticsearch-hprof
Source:         https://github.com/Szpadel/elasticsearch-hprof/archive/%{git_sha}.tar.gz
Source1:        elasticsearch-crash-handler.service
Source2:        elasticsearch-crash-handler.path

ExclusiveArch:  x86_64 aarch64

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

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain %{rust_toolchain}

%build
source $HOME/.cargo/env
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
* Thu Jan 18 2024 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 0.2.1-1
- New release

* Sat Jul 03 2021 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 0.1.0-2
- Fix typo in systemd service

* Tue Jun 01 2021 Piotr Rogowski <piotrekrogowski@gmail.com> - 0.1.0-1
- Initial package
