%global __provides_exclude_from ^(%{_libdir}/ags/.*\\.so)$

%global gvc_commit 8e7a5a4c3e51007ce6579292642517e3d3eb9c50
%global gvc_shortcommit %(c=%{gvc_commit}; echo ${c:0:7})

Name:           aylurs-gtk-shell
Version:        1.9.0
Release:        %autorelease -b2
Summary:        A customizable and extensible shell

License:        GPL-3.0-or-later
URL:            https://github.com/Aylur/ags
Source0:        %{url}/archive/v%{version_no_tilde}/%{name}-%{version_no_tilde}.tar.gz
Source2:        https://gitlab.gnome.org/GNOME/libgnome-volume-control/-/archive/%{gvc_commit}/gvc-%{gvc_shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  nodejs-npm
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gjs-1.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(pam)
BuildRequires:  typescript

Obsoletes:      aylurs-gtk-shell-git < 1.9.0

Requires:       gjs%{?_isa}
Requires:       gtk-layer-shell%{?_isa}
Requires:       libsoup3%{?_isa}

Recommends:     libdbusmenu-gtk3%{?_isa}
Recommends:     gnome-bluetooth-libs%{?_isa}

Provides:       bundled(libgnome-volume-control) = 0^1.git%{gvc_shortcommit}

%description
This program is essentially a library for gjs which allows defining GTK widgets
in a declarative way in JavaScript. It also provides services to interact with
the system so that these widgets can have functionality.

%prep
%autosetup -n ags-%{version_no_tilde} -p1
tar -xf %{SOURCE2} -C subprojects/gvc --strip=1

%build
npm install
%meson \
    -Dbuild_types=true \
    --libdir=%{_libdir}/ags
%meson_build

%install
%meson_install
# RPM build errors:
#    Symlink points to BuildRoot: /usr/bin/ags -> /builddir/build/BUILDROOT/aylurs-gtk-shell-1.7.4-1.fc39.x86_64//usr/share/com.github.Aylur.ags/com.github.Aylur.ags
rm %{buildroot}%{_bindir}/ags
ln -s %{_datadir}/com.github.Aylur.ags/com.github.Aylur.ags %{buildroot}%{_bindir}/ags

%files
%license LICENSE
%doc README.md
%doc example/
%{_bindir}/ags
%{_datadir}/com.github.Aylur.ags/
%{_libdir}/ags/
%{_sysconfdir}/pam.d/ags

%changelog
%autochangelog
