%global hyprland_commit 1a91c6ee603e3e779f288ad9189992faeda944f8
%global hyprland_shortcommit %(c=%{hyprland_commit}; echo ${c:0:7})

%global wlroots_commit 00489b11a0d926058d23584e2ad0e2b64f5b7406
%global wlroots_shortcommit %(c=%{wlroots_commit}; echo ${c:0:7})

%global protocols_commit 4d29e48433270a2af06b8bc711ca1fe5109746cd
%global protocols_shortcommit %(c=%{protocols_commit}; echo ${c:0:7})

%global udis86_commit 5336633af70f3917760a6d441ff02d93477b0c86
%global udis86_shortcommit %(c=%{udis86_commit}; echo ${c:0:7})

Name:           hyprland
Version:        0.24.1^12.git%{hyprland_shortcommit}
Release:        1%{?dist}
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks

License:        BSD-3-Clause AND MIT AND BSD-2-Clause
URL:            https://github.com/hyprwm/Hyprland
Source0:        %{url}/archive/%{hyprland_commit}/%{name}-%{hyprland_shortcommit}.tar.gz
Source1:        https://gitlab.freedesktop.org/wlroots/wlroots/-/archive/%{wlroots_commit}/wlroots-%{wlroots_shortcommit}.tar.gz
Source2:        https://github.com/hyprwm/hyprland-protocols/archive/%{protocols_commit}/protocols-%{protocols_shortcommit}.tar.gz
Source3:        https://github.com/canihavesomecoffee/udis86/archive/%{udis86_commit}/udis86-%{udis86_shortcommit}.tar.gz


BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  jq
BuildRequires:  git

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)

BuildRequires:  glslang
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xwayland)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libliftoff) >= 0.4.1

Requires:       pixman%{?_isa} >= 0.42.0
Requires:       pango%{?_isa}
Requires:       libliftoff%{?_isa} >= 0.4.1
Requires:       libwayland-server%{?_isa} >= 1.22.0

%description
Hyprland is a dynamic tiling Wayland compositor based on wlroots that doesn't
sacrifice on its looks.  It supports multiple layouts, fancy effects, has a
very flexible IPC model allowing for a lot of customization, a powerful 
plugin system and more.

%package devel
Summary:        Static library and header files for the %{name}
Recommends:     pkgconfig(xcb-icccm)
Suggests:       gcc
Suggests:       meson >= 0.58.0
Suggests:       pkgconfig(libpng)
Suggests:       pkgconfig(libavutil)
Suggests:       pkgconfig(libavcodec)
Suggests:       pkgconfig(libavformat)
Suggests:       pkgconfig(wayland-egl)
Conflicts:      wlroots-devel

%description devel
The %{name}-devel package contains API documentation for
developing %{name}.


%prep
%autosetup -n Hyprland-%{hyprland_commit} -p1
%setup -qn Hyprland-%{hyprland_commit} -DT -a1
%setup -qn Hyprland-%{hyprland_commit} -DT -a2
%setup -qn Hyprland-%{hyprland_commit} -DT -a3
sed -i 's|^GIT_COMMIT_HASH =.*|GIT_COMMIT_HASH = '\''%{hyprland_commit}'\''|' meson.build
sed -i 's|^GIT_DIRTY =.*|GIT_DIRTY = '\'''\''|' meson.build

mv hyprland-protocols-%{protocols_commit}/* subprojects/hyprland-protocols
mv wlroots-%{wlroots_commit}/* subprojects/wlroots
mv udis86-%{udis86_commit}/* subprojects/udis86


%build
%meson  -Dwlroots:examples=false \
        -Dwlroots:xcb-errors=disabled
%meson_build

%install
%meson_install

%files
%{_bindir}/Hyprland
%{_bindir}/hyprctl
%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*
%{_datadir}/hyprland/
%{_datadir}/wayland-sessions/hyprland.desktop

%files devel
%{_includedir}/wlr/
%{_libdir}/libwlroots.a
%{_libdir}/pkgconfig/wlroots.pc
%{_datadir}/pkgconfig/hyprland-protocols.pc
%{_datadir}/hyprland-protocols/


%changelog
