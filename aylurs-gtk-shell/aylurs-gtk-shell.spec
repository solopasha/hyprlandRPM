%global ver 1.5.4

%global __provides_exclude_from ^(%{_libdir}/ags/.*\\.so)$

%global gvc_commit 8e7a5a4c3e51007ce6579292642517e3d3eb9c50
%global gvc_shortcommit %(c=%{gvc_commit}; echo ${c:0:7})

Name:           aylurs-gtk-shell
Version:        %{ver}~beta
Release:        %autorelease
Summary:        A customizable and extensible shell

License:        GPL-3.0-or-later
URL:            https://github.com/Aylur/ags
Source0:        %{url}/archive/v%{version_no_tilde}/%{name}-%{version_no_tilde}.tar.gz
Source1:        %{url}/releases/download/v%{version_no_tilde}/node_modules-v%{version_no_tilde}.tar.gz
Source2:        https://gitlab.gnome.org/GNOME/libgnome-volume-control/-/archive/%{gvc_commit}/gvc-%{gvc_shortcommit}.tar.gz

BuildRequires:  meson
BuildRequires:  typescript
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gjs-1.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libpulse)

Requires:       gjs
Requires:       gtk-layer-shell

Recommends:     libdbusmenu-gtk3
Recommends:     gnome-bluetooth-libs

Provides:       bundled(libgnome-volume-control) = 0^1.git%{gvc_shortcommit}

%description
This program is essentially a library for gjs which allows defining GTK widgets
in a declarative way in JavaScript. It also provides services to interact with
the system so that these widgets can have functionality.


%prep
%autosetup -n ags-%{version_no_tilde}
%autosetup -n ags-%{version_no_tilde} -NDT -a1
tar -xf %{SOURCE2} -C subprojects/gvc --strip=1


%build
%meson --libdir=%{_libdir}/ags
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md
%doc example/
%{_bindir}/ags
%{_datadir}/com.github.Aylur.ags/
%{_libdir}/ags/


%changelog
%autochangelog
