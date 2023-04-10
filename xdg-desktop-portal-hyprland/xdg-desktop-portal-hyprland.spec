%global portal_commit 04f579377a32781ce57c9cf4ba2a5bcb7f53fa97
%global portal_shortcommit %(c=%{portal_commit}; echo ${c:0:7})

%global protocols_commit 4d29e48433270a2af06b8bc711ca1fe5109746cd
%global protocols_shortcommit %(c=%{protocols_commit}; echo ${c:0:7})


Name:           xdg-desktop-portal-hyprland
Epoch:          1
Version:        0.2.1^1.git%{portal_shortcommit}
Release:        1%{?dist}
Summary:        xdg-desktop-portal backend for hyprland

License:        MIT
URL:            https://github.com/hyprwm/%{name}
Source0:        %{url}/archive/%{portal_commit}/%{name}-%{version}.tar.gz
Source1:        https://github.com/hyprwm/hyprland-protocols/archive/%{protocols_commit}/protocols-%{protocols_shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(scdoc)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.24
BuildRequires:  pkgconfig(wayland-scanner)

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(uuid)

Requires:       dbus
# required for Screenshot portal implementation
Requires:       grim
Requires:       xdg-desktop-portal
# required for Screencast output selection.
# xdpw will try to use first available of the 3 utilities
Recommends:     (slurp or wofi or bemenu)
Suggests:       slurp

Enhances:       hyprland
Supplements:    (hyprland and (flatpak or snapd))

%description
%{summary}.
This project seeks to add support for the screenshot, screencast, and possibly
remote-desktop xdg-desktop-portal interfaces for wlroots based compositors.

%package devel
Summary:    Devel files for the %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{portal_commit}
%setup -qn %{name}-%{portal_commit} -DT -a1
mv hyprland-protocols-%{protocols_commit}/* subprojects/hyprland-protocols


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

%files devel
%{_datadir}/pkgconfig/hyprland-protocols.pc
%{_datadir}/hyprland-protocols/

%changelog
