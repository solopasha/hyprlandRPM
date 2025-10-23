%bcond wireplumber %[0%{?fedora} > 39]

%global commit0 161367d9617673a4ef9caf8299411dc5153464d1
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 5

Name:           waybar-git
Version:        0.14.0%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        1%{?dist}
Summary:        Highly customizable Wayland bar for Sway and Wlroots based compositors, with workspaces support for Hyprland
# Source files/overall project licensed as MIT, but
# - BSL-1.0
#   * include/util/clara.hpp
# - HPND-sell-variant
#   * protocol/ext-workspace-unstable-v1.xml
#   * protocol/wlr-foreign-toplevel-management-unstable-v1.xml
#   * protocol/wlr-layer-shell-unstable-v1.xml
# - ISC
#   * protocol/river-control-unstable-v1.xml
#   * protocol/river-status-unstable-v1.xml
#   * src/util/rfkill.cpp
License:        MIT AND BSL-1.0 AND ISC
URL:            https://github.com/Alexays/Waybar
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.49.0
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros
%if %{fedora} >= 40
BuildRequires:  pkgconfig(catch2)
%endif
BuildRequires:  pkgconfig(date)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(fmt) >= 8.1.1
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0)
BuildRequires:  pkgconfig(gtkmm-3.0)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libmpdclient)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libnl-genl-3.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(playerctl)
BuildRequires:  pkgconfig(sigc++-2.0)
BuildRequires:  pkgconfig(spdlog) >= 1.10.0
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
%if %{with wireplumber}
BuildRequires:  pkgconfig(wireplumber-0.5)
%endif
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(xkbregistry)
BuildRequires:  python3dist(packaging)
BuildRequires:  pkgconfig(libgps)

Conflicts:      waybar
Provides:       waybar

Enhances:       hyprland
Recommends:     (font(fontawesome6free) or font(fontawesome5free))

%description
%{summary}.

%prep
%autosetup -p1 -n Waybar-%{commit0}

%build
%meson \
%if %{fedora} < 40
    -Dtests=disabled \
%endif
    -Dsndio=disabled \
    -Dcava=disabled \
    %{!?with_wireplumber:-Dwireplumber=disabled}
%meson_build

%install
%meson_install
# remove man pages for disabled modules
for module in cava sndio %{!?with_wireplumber:wireplumber} wlr-workspaces; do
    rm -f %{buildroot}%{_mandir}/man5/%{name}-${module}.5
done

%check
%meson_test

%post
%systemd_user_post waybar.service

%preun
%systemd_user_preun waybar.service


%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/xdg/waybar
%config(noreplace) %{_sysconfdir}/xdg/waybar/config.jsonc
%config(noreplace) %{_sysconfdir}/xdg/waybar/style.css
%{_bindir}/waybar
%{_mandir}/man5/waybar*
%{_userunitdir}/waybar.service

%changelog
* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.17-1
- Update to 0.9.17
- Convert License tag to SPDX

* Thu Nov 24 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.16-1
- Update to 0.9.16 (#2139998)

* Thu Nov 03 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 0.9.13-4
- Rebuilt due to spdlog update.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 16 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.13-2
- Rebuild for fmt 9.0.0

* Mon May 23 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.13-1
- Update to 0.9.13 (#2089525)

* Thu Mar 10 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.12-1
- Update to 0.9.12 (#2062615)

* Sun Mar 06 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.10-1
- Update to 0.9.10 (#2061176)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.9-1
- Update to 0.9.9
- Install systemd user service

* Wed Nov 03 2021 Björn Esser <besser82@fedoraproject.org> - 0.9.8-3
- Rebuild (jsoncpp)

* Tue Nov 02 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.8-2
- Add patch for 'river/tags' protocol error on River

* Mon Aug 16 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.8-1
- Update to 0.9.8

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 05 2021 Richard Shaw <hobbes1069@gmail.com> - 0.9.7-3
- Rebuild for new fmt version.

* Tue Jun 15 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.7-2
- Add patch for waybar crash on disabling outputs

* Thu Apr 15 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.7-1
- Update to 0.9.7

* Thu Apr 15 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.6-1
- Update to 0.9.6

* Wed Feb 10 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.5-4
- Add patch for rfkill exception with kernel 5.11
- Fixes rhbz#1927821

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.5-2
- Fix build with spdlog 1.5 (f32)
- Add patch for possible crashes in 'wlr/taskbar'

* Wed Dec 23 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.5-1
- Update to 0.9.5

* Fri Nov 13 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.4-3
- Add patch for 'wlr/taskbar' protocol error with wlroots 0.12.0

* Tue Nov 03 2020 Jeff Law <law@redhat.com> - 0.9.4-2
- Fix mising #includes for gcc-11

* Mon Sep 21 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.4-1
- Update to 0.9.4

* Sun Sep 20 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.3-2
- Add patch for custom module signal handling regression
- Add patch for network module crash with fmt 7.0
- Add patch for broken updates in mpd and network modules

* Wed Aug 05 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.3-1
- Update to 0.9.3 (closes rhbz#1866571)
- Add patch for wlr/taskbar config strings

* Mon Aug 03 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.2-4
- Rebuild (date)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Björn Esser <besser82@fedoraproject.org> - 0.9.2-2
- Rebuild (jsoncpp)

* Sat Apr 11 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.2-1
- Update to 0.9.2

* Mon Feb 10 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.1-1
- Update to 0.9.1
- Remove upstreamed patch
- Add BuildRequires: pkgconfig(date)

* Sat Feb 08 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.9.0-1
- Initial import (#1798811)
