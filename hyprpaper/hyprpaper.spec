Name:           hyprpaper
Version:        0.4.0
Release:        %autorelease
Summary:        Blazing fast wayland wallpaper utility with IPC controls

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpaper
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

%description
Hyprpaper is a blazing fast wallpaper utility for Hyprland with the ability
to dynamically change wallpapers through sockets. It will work on all
wlroots-based compositors, though.

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
%autochangelog
