%global apiver 0

Name:           gtk4-layer-shell
Version:        1.0.2
Release:        %autorelease
Summary:        Library to create components for Wayland using the Layer Shell

License:        MIT
URL:            https://github.com/wmww/gtk4-layer-shell
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  lua-lgi-compat
BuildRequires:  luajit
BuildRequires:  meson
BuildRequires:  python3-gobject
BuildRequires:  vala

BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.

%prep
%autosetup -p1
sed -i '/test-lua-example/d' test/smoke-tests/meson.build
rm test/smoke-tests/test-lua-example.py

%build
%meson -Dtests=true -Dexamples=true
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_libdir}/girepository-1.0/Gtk4LayerShell-1.0.typelib
%{_libdir}/lib%{name}.so.%{version}
%{_libdir}/lib%{name}.so.%{apiver}

%files devel
%{_bindir}/gtk4-layer-demo
%{_datadir}/gir-1.0/Gtk4LayerShell-1.0.gir
%{_datadir}/vala/vapi/%{name}-%{apiver}*
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}-%{apiver}.pc

%changelog
%autochangelog
