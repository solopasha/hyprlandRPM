# Generated by rust2rpm 25
%bcond_with check

%global crate hyprnome

Name:           hyprnome
Version:        0.3.1
Release:        %autorelease -b2
Summary:        GNOME-like workspace switching in Hyprland
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# GPL-3.0-or-later
# MIT
# MIT OR Apache-2.0
# MIT OR Zlib OR Apache-2.0
# Unlicense OR MIT
License:        GPL-3.0-or-later AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND MIT AND (MIT OR Zlib OR Apache-2.0) AND (Unlicense OR MIT)
# LICENSE.dependencies contains a full license breakdown

URL:            https://github.com/donovanglover/hyprnome
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  gcc-c++

%global _description %{expand:
GNOME-like workspace switching in Hyprland.}

%description %{_description}

%prep
%autosetup -p1
cargo vendor
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
install -Dpm755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dpm644 target/completions/_%{name} %{buildroot}%{zsh_completions_dir}/_%{name}
install -Dpm644 target/completions/%{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -Dpm644 target/completions/%{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish
install -Dpm644 target/man/%{name}.1 -t %{buildroot}%{_mandir}/man1

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc CHANGELOG.md
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}

%changelog
%autochangelog
