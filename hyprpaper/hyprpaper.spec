Name:           hyprpaper
Version:        0.7.3
Release:        %autorelease -b3
Summary:        Blazing fast wayland wallpaper utility with IPC controls
# LICENSE: BSD-3-Clause
# protocols/wlr-layer-shell-unstable-v1.xml: HPND-sell-variant
License:        BSD-3-Clause AND HPND-sell-variant
URL:            https://github.com/hyprwm/hyprpaper
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch:          https://github.com/hyprwm/hyprpaper/commit/505e447b6c48e6b49f3aecf5da276f3cc5780054.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

%description
Hyprpaper is a blazing fast wallpaper utility for Hyprland with the ability
to dynamically change wallpapers through sockets. It will work on all
wlroots-based compositors, though.

%prep
%autosetup -p1
sed '/hyprpaper.service/s/${CMAKE_INSTALL_LIBDIR}/lib/' -i CMakeLists.txt
sed '/libjxl/d' -i CMakeLists.txt

%build
%cmake
%cmake_build

%install
%cmake_install

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service

%changelog
%autochangelog
