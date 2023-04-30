%global commit0 5c383dc5bc91afabe7dbcafdfd17f577fe4dcf96
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global __provides_exclude_from ^(%{_libdir}/hyprland/.*\\.so)$

%global plugins %{expand:borders-plus-plus csgo-vulkan-fix hyprbars}

Name:           hyprland-plugins
Version:        0.1
Release:        %autorelease -b 3
Summary:        Official plugins for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-plugins
Source:         %{url}/archive/%{commit0}/%{name}-%{commit0}.tar.gz
Patch:          fix-paths.patch

BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprland)
BuildRequires:  pkgconfig(cairo)

%description
%{summary}.

%define _package() \%package -n hyprland-plugin-%1\
Summary:       %1 plugin for hyprland\
Requires:      hyprland\
Requires:      \%{name} = \%{version}-\%{release}\
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
