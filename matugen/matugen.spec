%bcond_with check

Name:           matugen
Version:        2.4.1
Release:        %autorelease
Summary:        A material you color generation tool with templates
License:        GPL-2.0-only

URL:            https://github.com/InioX/matugen
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
%{summary}.}

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
install -Dpm755 target/release/matugen %{buildroot}%{_bindir}/matugen

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
%{_bindir}/matugen

%changelog
%autochangelog
