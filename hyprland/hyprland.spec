%global hyprland_commit 28ca434fb52befa2058a6c23b21566c280654e03
%global hyprland_shortcommit %(c=%{hyprland_commit}; echo ${c:0:7})
%global bumpver 14

%global wlroots_commit 00489b11a0d926058d23584e2ad0e2b64f5b7406
%global wlroots_shortcommit %(c=%{wlroots_commit}; echo ${c:0:7})

%global protocols_commit 4d29e48433270a2af06b8bc711ca1fe5109746cd
%global protocols_shortcommit %(c=%{protocols_commit}; echo ${c:0:7})

%global udis86_commit 5336633af70f3917760a6d441ff02d93477b0c86
%global udis86_shortcommit %(c=%{udis86_commit}; echo ${c:0:7})

Name:           hyprland
Version:        0.24.1%{?bumpver:^%{bumpver}.git%{hyprland_shortcommit}}
Release:        1%{?dist}
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks

# hyprland: BSD-3-Clause
# subprojects/hyprland-protocols BSD-3-Clause
# subprojects/wlroots: MIT
# subproject/udis86: BSD-2-Clause
# protocols/ext-workspace-unstable-v1.xml: HPND-sell-variant
# protocols/wlr-foreign-toplevel-management-unstable-v1.xml: HPND-sell-variant
# protocols/wlr-layer-shell-unstable-v1.xml: HPND-sell-variant
# protocols/idle.xml: LGPL-2.1-or-later
License:        BSD-3-Clause AND MIT AND BSD-2-Clause AND HPND-sell-variant AND LGPL-2.1-or-later
URL:            https://github.com/hyprwm/Hyprland
%if 0%{?bumpver}
Source0:        %{url}/archive/%{hyprland_commit}/%{name}-%{hyprland_shortcommit}.tar.gz
Source1:        https://gitlab.freedesktop.org/wlroots/wlroots/-/archive/%{wlroots_commit}/wlroots-%{wlroots_shortcommit}.tar.gz
Source2:        https://github.com/hyprwm/hyprland-protocols/archive/%{protocols_commit}/protocols-%{protocols_shortcommit}.tar.gz
Source3:        https://github.com/canihavesomecoffee/udis86/archive/%{udis86_commit}/udis86-%{udis86_shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/v%{version}/source-v%{version}.tar.gz
%endif

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

# Upstream insists on always building against very current snapshots of
# wlroots, and doesn't provide a method for building against a system copy.
# https://github.com/hyprwm/Hyprland/issues/302
Provides:       bundled(wlroots) = 0.17.0~^1.%{wlroots_shortcommit}

# udis86 is packaged in Fedora, but the copy bundled here is actually a
# modified fork.
Provides:       bundled(udis86) = 1.7.2^1.%{udis86_shortcommit}

Requires:       pixman%{?_isa} >= 0.42.0
Requires:       pango%{?_isa}
Requires:       libliftoff%{?_isa} >= 0.4.1
Requires:       libwayland-server%{?_isa} >= 1.22.0

%description
Hyprland is a dynamic tiling Wayland compositor based on wlroots that doesn't
sacrifice on its looks.  It supports multiple layouts, fancy effects, has a
very flexible IPC model allowing for a lot of customization, a powerful
plugin system and more.

%package        protocols-devel
Summary:        Protocol files for the %{name}
License:        BSD-3-Clause

%description    protocols-devel
%{summary}.


%prep
%autosetup -n %{?bumpver:Hyprland-%{hyprland_commit}} %{!?bumpver:%{name}-source} -p1
%if 0%{?bumpver}
%setup -qn Hyprland-%{hyprland_commit} -DT -a1
%setup -qn Hyprland-%{hyprland_commit} -DT -a2
%setup -qn Hyprland-%{hyprland_commit} -DT -a3
mv hyprland-protocols-%{protocols_commit}/* subprojects/hyprland-protocols
mv wlroots-%{wlroots_commit}/* subprojects/wlroots
mv udis86-%{udis86_commit}/* subprojects/udis86

sed -i 's|^GIT_COMMIT_HASH =.*|GIT_COMMIT_HASH = '\''%{hyprland_commit}'\''|' meson.build
sed -i 's|^GIT_DIRTY =.*|GIT_DIRTY = '\'''\''|' meson.build
%endif
cp subprojects/hyprland-protocols/LICENSE LICENSE-hyprland-protocols
cp subprojects/udis86/LICENSE LICENSE-udis86
cp subprojects/wlroots/LICENSE LICENSE-wlroots

%build
%meson  -Dwlroots:examples=false \
        -Dwlroots:xcb-errors=disabled
%meson_build

%install
%meson_install

rm -r %{buildroot}%{_includedir}/wlr
rm -r %{buildroot}%{_libdir}/libwlroots.a
rm -r %{buildroot}%{_libdir}/pkgconfig/wlroots.pc

%files
%license LICENSE LICENSE-udis86 LICENSE-wlroots
%{_bindir}/Hyprland
%{_bindir}/hyprctl
%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*
%{_datadir}/hyprland/
%{_datadir}/wayland-sessions/hyprland.desktop

%files protocols-devel
%license LICENSE-hyprland-protocols
%{_datadir}/pkgconfig/hyprland-protocols.pc
%{_datadir}/hyprland-protocols/


%changelog
