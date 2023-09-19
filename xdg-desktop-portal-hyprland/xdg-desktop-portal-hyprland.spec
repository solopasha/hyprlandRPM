%global portal_commit ca077cc05c370879a6df90eac43a3c2ee6768306
%global portal_shortcommit %(c=%{portal_commit}; echo ${c:0:7})
#global bumpver 1

Name:           xdg-desktop-portal-hyprland
Epoch:          1
Version:        1.1.0%{?bumpver:^%{bumpver}.git%{portal_shortcommit}}
Release:        %autorelease
Summary:        xdg-desktop-portal backend for hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/%{name}
%if 0%{?bumpver}
Source:         %{url}/archive/%{portal_commit}/%{name}-%{version}.tar.gz
%else
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)

Requires:       dbus
# required for Screenshot portal implementation
Requires:       grim
Requires:       xdg-desktop-portal
# required for hyprland-share-picker
Requires:       slurp
Requires:       qt6-qtwayland

Enhances:       hyprland
Supplements:    hyprland
Supplements:    hyprland-nvidia
Supplements:    hyprland-legacyrenderer
Supplements:    hyprland-git
Supplements:    hyprland-nvidia-git

%description
%{summary}.


%prep
%autosetup %{?bumpver:-n %{name}-%{portal_commit}}


%build
%meson
%meson_build


%install
%meson_install


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
