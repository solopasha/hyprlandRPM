%global ver 1.2.0

%global __provides_exclude_from ^(%{_libdir}/ags/.*\\.so)$

%global gi_types_commit eb2a87a25c5e2fb580b605fbec0bd312fe34c492
%global gi_types_shortcommit %(c=%{gi_types_commit}; echo ${c:0:7})

%global gvc_commit 8e7a5a4c3e51007ce6579292642517e3d3eb9c50
%global gvc_shortcommit %(c=%{gvc_commit}; echo ${c:0:7})

Name:           aylurs-gtk-shell
Version:        %{ver}~beta
Release:        %autorelease -b3
Summary:        A customizable and extensible shell

License:        GPL-3.0-or-later
URL:            https://github.com/Aylur/ags
Source0:        %{url}/archive/v%{ver}/%{name}-%{version_no_tilde}.tar.gz
Source1:        https://gitlab.gnome.org/BrainBlasted/gi-typescript-definitions/-/archive/%{gi_types_commit}/gi-types-%{gi_types_shortcommit}.tar.gz
Source2:        https://gitlab.gnome.org/GNOME/libgnome-volume-control/-/archive/%{gvc_commit}/gvc-%{gvc_shortcommit}.tar.gz

BuildRequires:  meson
BuildRequires:  /usr/bin/npm
BuildRequires:  typescript
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gjs-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libpulse)
Requires:       gjs
Requires:       gtk-layer-shell
Recommends:     libdbusmenu-gtk3
Recommends:     gnome-bluetooth-libs

Provides:       bundled(gi-typescript-definitions) = 0^1.git%{gi_types_shortcommit}
Provides:       bundled(libgnome-volume-control) = 0^1.git%{gvc_shortcommit}

%description
This program is essentially a library for gjs which allows defining GTK widgets
in a declarative way in JavaScript. It also provides services to interact with
the system so that these widgets can have functionality.


%prep
%autosetup -n ags-%{ver}
tar -xf %{SOURCE1} -C gi-types --strip=1
tar -xf %{SOURCE2} -C subprojects/gvc --strip=1


%build
npm install
%meson
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md
%{_bindir}/ags
%{_datadir}/ags/
%{_libdir}/ags/


%changelog
%autochangelog
