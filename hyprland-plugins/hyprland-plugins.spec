%global commit0 dbac31172965f22a3725e55cf20b17c8d2f38961
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 15

%global __provides_exclude_from ^(%{_libdir}/hyprland/.*\\.so)$

%global plugins %{expand:borders-plus-plus csgo-vulkan-fix hyprbars hyprtrails}

Name:           hyprland-plugins
Version:        0.1^%{bumpver}.git%{shortcommit0}
Release:        %autorelease
Summary:        Official plugins for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-plugins
Source:         %{url}/archive/%{commit0}/%{name}-%{commit0}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  hyprland-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput) >= 1.23.0
BuildRequires:  pkgconfig(libliftoff) >= 0.4.1
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1) >= 0.42.0
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.22.0
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xwayland)

# print Recommends: for each plugin
%{lua:for w in rpm.expand('%plugins'):gmatch("%S+") do print("Recommends: hyprland-plugin-"..w..'\n') end}

%description
%{summary}.

%define _package() \%package -n hyprland-plugin-%1\
Summary:       %1 plugin for hyprland\
Requires:      hyprland = %_hyprland_version\
\%description  -n hyprland-plugin-%1\
\%1 plugin for hyprland.\
\%files -n     hyprland-plugin-%1\
\%%license LICENSE\
\%dir %{_libdir}/hyprland\
\%{_libdir}/hyprland/lib%1.so\

# expand %%_package for each plugin
%{lua:for w in rpm.expand('%plugins'):gmatch("%S+") do print(rpm.expand("%_package "..w)..'\n\n') end}


%prep
%autosetup -n %{name}-%{commit0} -p1


%build
for plugin in %{plugins}
do
pushd $plugin
%meson --libdir=%{_libdir}/hyprland
%meson_build
popd
done


%install
for plugin in %{plugins}
do
pushd $plugin
%meson_install
popd
done


%files


%changelog
%autochangelog
