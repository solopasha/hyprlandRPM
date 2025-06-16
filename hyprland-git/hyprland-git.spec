%global hyprland_commit d4e8a440874bebed07a5908009a3d854120277ed
%global hyprland_shortcommit %(c=%{hyprland_commit}; echo ${c:0:7})
%global bumpver 57
%global commits_count 6196
%global commit_date Sun Jun 15 23:42:58 2025

%global protocols_commit 3a5c2bda1c1a4e55cc1330c782547695a93f05b2
%global protocols_shortcommit %(c=%{protocols_commit}; echo ${c:0:7})

%global udis86_commit 5336633af70f3917760a6d441ff02d93477b0c86
%global udis86_shortcommit %(c=%{udis86_commit}; echo ${c:0:7})

Name:           hyprland-git
Version:        0.49.0%{?bumpver:^%{bumpver}.git%{hyprland_shortcommit}}
Release:        %autorelease
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks

# hyprland: BSD-3-Clause
# subprojects/hyprland-protocols: BSD-3-Clause
# subproject/udis86: BSD-2-Clause
# protocols/ext-workspace-unstable-v1.xml: HPND-sell-variant
# protocols/wlr-foreign-toplevel-management-unstable-v1.xml: HPND-sell-variant
# protocols/wlr-layer-shell-unstable-v1.xml: HPND-sell-variant
# protocols/idle.xml: LGPL-2.1-or-later
License:        BSD-3-Clause AND BSD-2-Clause AND HPND-sell-variant AND LGPL-2.1-or-later
URL:            https://github.com/hyprwm/Hyprland
%if 0%{?bumpver}
Source0:        %{url}/archive/%{hyprland_commit}/%{name}-%{hyprland_shortcommit}.tar.gz
Source2:        https://github.com/hyprwm/hyprland-protocols/archive/%{protocols_commit}/protocols-%{protocols_shortcommit}.tar.gz
Source3:        https://github.com/canihavesomecoffee/udis86/archive/%{udis86_commit}/udis86-%{udis86_shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/v%{version}/source-v%{version}.tar.gz
%endif
Source4:        macros.hyprland

%{lua:
hyprdeps = {
    "cmake",
    "gcc-c++",
    "git-core",
    "meson",
    "glaze-static",
    "pkgconfig(aquamarine)",
    "pkgconfig(cairo)",
    "pkgconfig(egl)",
    "pkgconfig(gbm)",
    "pkgconfig(gio-2.0)",
    "pkgconfig(glesv2)",
    "pkgconfig(hwdata)",
    "pkgconfig(hyprcursor)",
    "pkgconfig(hyprgraphics)",
    "pkgconfig(hyprlang)",
    "pkgconfig(hyprutils)",
    "pkgconfig(hyprwayland-scanner)",
    "pkgconfig(libdisplay-info)",
    "pkgconfig(libdrm)",
    "pkgconfig(libinput)",
    "pkgconfig(libliftoff)",
    "pkgconfig(libseat)",
    "pkgconfig(libudev)",
    "pkgconfig(pango)",
    "pkgconfig(pangocairo)",
    "pkgconfig(pixman-1)",
    "pkgconfig(re2)",
    "pkgconfig(systemd)",
    "pkgconfig(tomlplusplus)",
    "pkgconfig(uuid)",
    "pkgconfig(wayland-client)",
    "pkgconfig(wayland-protocols)",
    "pkgconfig(wayland-scanner)",
    "pkgconfig(wayland-server)",
    "pkgconfig(xcb-composite)",
    "pkgconfig(xcb-dri3)",
    "pkgconfig(xcb-errors)",
    "pkgconfig(xcb-ewmh)",
    "pkgconfig(xcb-icccm)",
    "pkgconfig(xcb-present)",
    "pkgconfig(xcb-render)",
    "pkgconfig(xcb-renderutil)",
    "pkgconfig(xcb-res)",
    "pkgconfig(xcb-shm)",
    "pkgconfig(xcb-util)",
    "pkgconfig(xcb-xfixes)",
    "pkgconfig(xcb-xinput)",
    "pkgconfig(xcb)",
    "pkgconfig(xcursor)",
    "pkgconfig(xkbcommon)",
    "pkgconfig(xwayland)",
    }
}

%define printbdeps(r) %{lua:
for _, dep in ipairs(hyprdeps) do
    print((rpm.expand("%{-r}") ~= "" and "Requires: " or "BuildRequires: ")..dep.."\\n")
end
}

%printbdeps

# udis86 is packaged in Fedora, but the copy bundled here is actually a
# modified fork.
Provides:       bundled(udis86) = 1.7.2^1.%{udis86_shortcommit}

Requires:       xorg-x11-server-Xwayland%{?_isa}
Requires:       hyprcursor%{?_isa} >= 0.1.9
Requires:       hyprgraphics%{?_isa} >= 0.1.3

%{lua:do
if string.match(rpm.expand('%{name}'), '%-git$') then
    print('Conflicts: hyprland'..'\n')
    print('Obsoletes: hyprland-nvidia-git < 0.32.3^30.gitad3f688-2'..'\n')
    print(rpm.expand('Provides: hyprland-nvidia-git = %{version}-%{release}')..'\n')
    print('Obsoletes: hyprland-aquamarine-git < 0.41.2^20.git4b84029-2'..'\n')
elseif not string.match(rpm.expand('%{name}'), 'hyprland$') then
    print(rpm.expand('Provides: hyprland = %{version}-%{release}')..'\n')
    print('Conflicts: hyprland'..'\n')
else
    print('Obsoletes: hyprland-nvidia < 1:0.32.3-2'..'\n')
    print(rpm.expand('Provides: hyprland-nvidia = %{version}-%{release}')..'\n')
    print('Obsoletes: hyprland-legacyrenderer < 0.49.0'..'\n')
end
end}

# Used in the default configuration
Recommends:     kitty
Recommends:     wofi
Recommends:     playerctl
Recommends:     brightnessctl
Recommends:     hyprland-qtutils
# Lack of graphical drivers may hurt the common use case
Recommends:     mesa-dri-drivers
# Logind needs polkit to create a graphical session
Recommends:     polkit
# https://wiki.hyprland.org/Useful-Utilities/Systemd-start
Recommends:     %{name}-uwsm

Recommends:     (qt5-qtwayland if qt5-qtbase-gui)
Recommends:     (qt6-qtwayland if qt6-qtbase-gui)

%description
Hyprland is a dynamic tiling Wayland compositor that doesn't sacrifice
on its looks. It supports multiple layouts, fancy effects, has a
very flexible IPC model allowing for a lot of customization, a powerful
plugin system and more.

%package        uwsm
Summary:        Files for a uwsm-managed session
Requires:       uwsm
%description    uwsm
Files for a uwsm-managed session.

%package        devel
Summary:        Header and protocol files for %{name}
License:        BSD-3-Clause
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cpio
%{lua:do
if string.match(rpm.expand('%{name}'), 'hyprland%-git$') then
    print('Obsoletes: hyprland-nvidia-git-devel < 0.32.3^30.gitad3f688-2'..'\n')
    print(rpm.expand('Provides: hyprland-nvidia-git-devel = %{version}-%{release}')..'\n')
    print('Obsoletes: hyprland-aquamarine-git-devel < 0.41.2^20.git4b84029-2'..'\n')
elseif string.match(rpm.expand('%{name}'), 'hyprland$') then
    print('Obsoletes: hyprland-nvidia-devel < 1:0.32.3-2'..'\n')
    print(rpm.expand('Provides: hyprland-nvidia-devel = %{version}-%{release}')..'\n')
end
end}
%printbdeps -r

%description    devel
%{summary}.


%prep
%autosetup -n %{?bumpver:Hyprland-%{hyprland_commit}} %{!?bumpver:hyprland-source} -N

%if 0%{?bumpver}
tar -xf %{SOURCE2} -C subprojects/hyprland-protocols --strip=1
tar -xf %{SOURCE3} -C subprojects/udis86 --strip=1
sed -e 's|^HASH=.*|HASH=%{hyprland_commit}|' \
    -e 's|^DIRTY=.*|DIRTY=|' \
    -e 's|^BRANCH=.*|BRANCH=main|' \
    -e 's|^DATE=.*|DATE="%{commit_date}"|' \
    -e 's|^COMMITS=.*|COMMITS=%{commits_count}|' \
    -i scripts/generateVersion.sh
%endif

cp -p subprojects/hyprland-protocols/LICENSE LICENSE-hyprland-protocols
cp -p subprojects/udis86/LICENSE LICENSE-udis86

sed -i \
  -e "s|@@HYPRLAND_VERSION@@|%{version}|g" \
  %{SOURCE4}


%build
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release
%cmake_build


%install
%cmake_install
install -Dpm644 %{SOURCE4} -t %{buildroot}%{_rpmconfigdir}/macros.d


%files
%license LICENSE LICENSE-udis86 LICENSE-hyprland-protocols
%{_bindir}/[Hh]yprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_datadir}/hypr/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_mandir}/man1/hyprctl.1*
%{_mandir}/man1/Hyprland.1*
%{bash_completions_dir}/hypr*
%{fish_completions_dir}/hypr*.fish
%{zsh_completions_dir}/_hypr*

%files uwsm
%{_datadir}/wayland-sessions/hyprland-uwsm.desktop

%files devel
%{_datadir}/pkgconfig/hyprland.pc
%{_includedir}/hyprland/
%{_rpmconfigdir}/macros.d/macros.hyprland


%changelog
%autochangelog
