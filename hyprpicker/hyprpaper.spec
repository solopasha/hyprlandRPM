Name:           hyprpicker
Version:        0.1.0
Release:        2%{?dist}
Summary:        A wlroots-compatible Wayland color picker

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpicker
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

%description
%{summary}.

%prep
%autosetup


%build
make protocols
%cmake
%cmake_build


%install
install -m0755 -Dp %{__cmake_builddir}/%{name} %{buildroot}%{_bindir}/%{name}


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Sun Apr 30 2023 Pavel Solovev <daron439@gmail.com> - 0.1.0-2
- Initial packaging
