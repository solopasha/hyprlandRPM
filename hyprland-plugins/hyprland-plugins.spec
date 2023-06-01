%global commit0 e368bd15e4bfd560baa9333ad47415340c563458
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global __provides_exclude_from ^(%{_libdir}/hyprland/.*\\.so)$

%global plugins %{expand:borders-plus-plus csgo-vulkan-fix hyprbars}

Name:           hyprland-plugins
Version:        0.1^4.git%{shortcommit0}
Release:        %autorelease
Summary:        Official plugins for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-plugins
Source:         %{url}/archive/%{commit0}/%{name}-%{commit0}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprland)
BuildRequires:  pkgconfig(pangocairo)

Recommends:     hyprland-plugin-borders-plus-plus
Recommends:     hyprland-plugin-csgo-vulkan-fix
Recommends:     hyprland-plugin-hyprbars

%description
%{summary}.

%define _package() \%package -n hyprland-plugin-%1\
Summary:       %1 plugin for hyprland\
\%description  -n hyprland-plugin-%1\
\%{summary}.\
\%files -n     hyprland-plugin-%1\
\%{_libdir}/hyprland/lib%1.so\


%_package borders-plus-plus
%_package csgo-vulkan-fix
%_package hyprbars

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
%dir %{_libdir}/hyprland
%license LICENSE
%doc README.md

%changelog
%autochangelog
