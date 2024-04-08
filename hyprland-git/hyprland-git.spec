%global hyprland_commit 277f2bb76ace017e54c3bd8ea1a754e77350455a
%global hyprland_shortcommit %(c=%{hyprland_commit}; echo ${c:0:7})
%global bumpver 7

%global wlroots_commit 50eae512d9cecbf0b3b1898bb1f0b40fa05fe19b
%global wlroots_shortcommit %(c=%{wlroots_commit}; echo ${c:0:7})

%global protocols_commit 0c2ce70625cb30aef199cb388f99e19a61a6ce03
%global protocols_shortcommit %(c=%{protocols_commit}; echo ${c:0:7})

%global udis86_commit 5336633af70f3917760a6d441ff02d93477b0c86
%global udis86_shortcommit %(c=%{udis86_commit}; echo ${c:0:7})

%bcond legacyrenderer 0

Name:           hyprland-git
Version:        0.38.1%{?bumpver:^%{bumpver}.git%{hyprland_shortcommit}}
Release:        %autorelease
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks

# hyprland: BSD-3-Clause
# subprojects/hyprland-protocols: BSD-3-Clause
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
Source4:        macros.hyprland

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  jq
BuildRequires:  meson

%{lua:
hyprdeps = {
    "pkgconfig(cairo)",
    "pkgconfig(egl)",
    "pkgconfig(gbm)",
    "pkgconfig(glesv2)",
    "pkgconfig(hwdata)",
    "pkgconfig(hyprcursor)",
    "pkgconfig(hyprlang)",
    "pkgconfig(libdisplay-info)",
    "pkgconfig(libdrm)",
    "pkgconfig(libinput)",
    "pkgconfig(libliftoff)",
    "pkgconfig(libseat)",
    "pkgconfig(libudev)",
    "pkgconfig(pango)",
    "pkgconfig(pangocairo)",
    "pkgconfig(pixman-1)",
    "pkgconfig(tomlplusplus)",
    "pkgconfig(wayland-client)",
    "pkgconfig(wayland-protocols)",
    "pkgconfig(wayland-scanner)",
    "pkgconfig(wayland-server)",
    "pkgconfig(xcb-composite)",
    "pkgconfig(xcb-dri3)",
    "pkgconfig(xcb-icccm)",
    "pkgconfig(xcb-present)",
    "pkgconfig(xcb-render)",
    "pkgconfig(xcb-renderutil)",
    "pkgconfig(xcb-res)",
    "pkgconfig(xcb-shm)",
    "pkgconfig(xcb-xfixes)",
    "pkgconfig(xcb-xinput)",
    "pkgconfig(xcb)",
    "pkgconfig(xkbcommon)",
    "pkgconfig(xwayland)"
    }
}

%define printbdeps(r) %{lua:
for _, dep in ipairs(hyprdeps) do
    print((rpm.expand("%{-r}") ~= "" and "Requires: " or "BuildRequires: ")..dep.."\\n")
end
}

%printbdeps

# Upstream insists on always building against very current snapshots of
# wlroots, and doesn't provide a method for building against a system copy.
# https://github.com/hyprwm/Hyprland/issues/302
Provides:       bundled(wlroots) = 0.18.0~^1.%{wlroots_shortcommit}

# udis86 is packaged in Fedora, but the copy bundled here is actually a
# modified fork.
Provides:       bundled(udis86) = 1.7.2^1.%{udis86_shortcommit}

Requires:       libdrm%{?_isa} >= 2.4.120
Requires:       libliftoff%{?_isa} >= 0.4.1
Requires:       xorg-x11-server-Xwayland%{?_isa} >= 23.1.2

%{lua:do
if string.match(rpm.expand('%{name}'), '%-git$') then
    print('Conflicts: hyprland'..'\n')
    print('Obsoletes: hyprland-nvidia-git < 0.32.3^30.gitad3f688-2'..'\n')
    print(rpm.expand('Provides: hyprland-nvidia-git = %{version}-%{release}')..'\n')
elseif not string.match(rpm.expand('%{name}'), 'hyprland$') then
    print(rpm.expand('Provides: hyprland = %{version}-%{release}')..'\n')
    print('Conflicts: hyprland'..'\n')
else
    print('Obsoletes: hyprland-nvidia < 1:0.32.3-2'..'\n')
    print(rpm.expand('Provides: hyprland-nvidia = %{version}-%{release}')..'\n')
end
end}

# Both are used in the default configuration
Recommends:     kitty
Recommends:     wofi
# Lack of graphical drivers may hurt the common use case
Recommends:     mesa-dri-drivers
# Logind needs polkit to create a graphical session
Recommends:     polkit

Recommends:     (qt5-qtwayland if qt5-qtbase-gui)
Recommends:     (qt6-qtwayland if qt6-qtbase-gui)

%description
Hyprland is a dynamic tiling Wayland compositor based on wlroots that doesn't
sacrifice on its looks. It supports multiple layouts, fancy effects, has a
very flexible IPC model allowing for a lot of customization, a powerful
plugin system and more.

%package        devel
Summary:        Header and protocol files for %{name}
License:        BSD-3-Clause AND MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Recommends:     git-core
Requires:       cmake
Requires:       cpio
Requires:       meson
Requires:       ninja-build
%{lua:do
if string.match(rpm.expand('%{name}'), 'hyprland%-git$') then
    print('Obsoletes: hyprland-nvidia-git-devel < 0.32.3^30.gitad3f688-2'..'\n')
    print(rpm.expand('Provides: hyprland-nvidia-git-devel = %{version}-%{release}')..'\n')
elseif string.match(rpm.expand('%{name}'), 'hyprland$') then
    print('Obsoletes: hyprland-nvidia-devel < 1:0.32.3-2'..'\n')
    print(rpm.expand('Provides: hyprland-nvidia-devel = %{version}-%{release}')..'\n')
end
end}
%printbdeps -r

%description    devel
%{summary}.


%prep
%autosetup -n %{?bumpver:Hyprland-%{hyprland_commit}} %{!?bumpver:hyprland-source} -p1

%if 0%{?bumpver}
tar -xf %{SOURCE1} -C subprojects/wlroots --strip=1
tar -xf %{SOURCE2} -C subprojects/hyprland-protocols --strip=1
tar -xf %{SOURCE3} -C subprojects/udis86 --strip=1
sed -e 's|^HASH=.*|HASH=%{hyprland_commit}|' \
    -e 's|^DIRTY=.*|DIRTY=|' \
    -e 's|^BRANCH=.*|BRANCH=main|' \
    -i scripts/generateVersion.sh
%endif

cp -p subprojects/hyprland-protocols/LICENSE LICENSE-hyprland-protocols
cp -p subprojects/udis86/LICENSE LICENSE-udis86
cp -p subprojects/wlroots/LICENSE LICENSE-wlroots

sed -i \
  -e "s|@@HYPRLAND_VERSION@@|%{version}|g" \
  %{SOURCE4}


%build
%meson \
%if %{with legacyrenderer}
       -Dlegacy_renderer=enabled \
%endif
       -Dwlroots:examples=false \
       -Dwlroots:xcb-errors=disabled
%meson_build


%install
%meson_install
install -Dpm644 %{SOURCE4} -t %{buildroot}%{_rpmconfigdir}/macros.d
rm %{buildroot}%{_libdir}/libwlroots.a
rm %{buildroot}%{_libdir}/pkgconfig/wlroots.pc
mkdir -p %{buildroot}%{_includedir}/hyprland/wlroots/wlr \
         %{buildroot}%{bash_completions_dir} \
         %{buildroot}%{fish_completions_dir}
mv %{buildroot}%{_includedir}/wlr %{buildroot}%{_includedir}/hyprland/wlroots
mv %{buildroot}%{_datadir}/bash-completions/hyprctl %{buildroot}%{bash_completions_dir}/hyprctl
mv %{buildroot}%{_datadir}/fish/completions/hyprctl.fish %{buildroot}%{fish_completions_dir}/hyprctl.fish

%files
%license LICENSE LICENSE-udis86 LICENSE-wlroots LICENSE-hyprland-protocols
%{_bindir}/hyprctl
%{_bindir}/Hyprland
%{_bindir}/hyprpm
%{_datadir}/hyprland/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_mandir}/man1/hyprctl.1*
%{_mandir}/man1/Hyprland.1*
%{bash_completions_dir}/hyprctl
%{fish_completions_dir}/hyprctl.fish
%{zsh_completions_dir}/_hyprctl

%files devel
%{_datadir}/hyprland-protocols/
%{_datadir}/pkgconfig/hyprland*.pc
%{_includedir}/hyprland/
%{_rpmconfigdir}/macros.d/macros.hyprland


%changelog
%autochangelog
