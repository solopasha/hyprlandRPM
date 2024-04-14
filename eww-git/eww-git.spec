%global commit0 1e37f53e99016aa2cd725d7050788bb5d4fcc76a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 9

Name:           eww-git
Version:        0.5.0%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        %autorelease
Summary:        ElKowars wacky widgets

License:        MIT
URL:            https://github.com/elkowar/eww
Source:         %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cargo-rpm-macros
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  pkgconfig(dbusmenu-glib-0.4)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0)

Obsoletes:      eww-wayland-git < 0.5.0^5.gitf1ec00a-2
Provides:       eww-wayland-git = %{version}-%{release}

Provides:       eww
Provides:       eww-wayland

%description
Elkowars Wacky Widgets is a standalone widget system made in Rust that
allows you to implement your own, custom widgets in any window manager.

%prep
%autosetup -n eww-%{commit0}
cargo vendor
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
install -Dm755 target/release/eww -t %{buildroot}%{_bindir}

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc examples/ README.md
%{_bindir}/eww

%changelog
%autochangelog
