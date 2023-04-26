%global portal_commit c0e233955568fbea4e859336f6d3d14d51294d7c
%global portal_shortcommit %(c=%{portal_commit}; echo ${c:0:7})
#global bumpver 2

Name:           xdg-desktop-portal-hyprland
Epoch:          1
Version:        0.3.1%{?bumpver:^%{bumpver}.git%{portal_shortcommit}}
Release:        %autorelease
Summary:        xdg-desktop-portal backend for hyprland

License:        MIT
URL:            https://github.com/hyprwm/%{name}
%if 0%{?bumpver}
Source:         %{url}/archive/%{portal_commit}/%{name}-%{version}.tar.gz
%else
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build

BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(scdoc)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.24
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  systemd-rpm-macros


Requires:       dbus
# required for Screenshot portal implementation
Requires:       grim
Requires:       xdg-desktop-portal
# required for hyprland-share-picker
Requires:       slurp

Enhances:       hyprland
Supplements:    (hyprland and (flatpak or snapd))

%description
%{summary}.


%prep
%autosetup %{?bumpver:-n %{name}-%{portal_commit}}


%build
%meson \
    -Dsd-bus-provider=libsystemd
%meson_build
cd hyprland-share-picker
%cmake -G Ninja
%cmake_build


%install
%meson_install
cd hyprland-share-picker
%cmake_install

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service


%files
%license LICENSE
%doc README.md contrib/config.sample
%{_bindir}/hyprland-share-picker
%{_libexecdir}/%{name}
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_datadir}/dbus-1/services/*.service
%{_userunitdir}/%{name}.service


%changelog
%autochangelog
