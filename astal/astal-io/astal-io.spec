%global astal_commit 7f2292f0792ffc9b127d4788b3dd3f104b5374b2
%global astal_shortcommit %(c=%{astal_commit}; echo ${c:0:7})
%global bumpver 6

%global _vpath_srcdir lib/astal/io

Name:           astal-io
Version:        0~%{bumpver}.git%{astal_shortcommit}
Release:        %autorelease
Summary:        Building blocks for creating custom desktop shells

License:        LGPL-2.1-only
URL:            https://github.com/Aylur/astal
Source0:        %{url}/archive/%{astal_commit}/%{name}-%{astal_shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  python3
BuildRequires:  vala
BuildRequires:  valadoc
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Development files for %{name}.

%description
%{summary}.

%prep
%autosetup -n astal-%{astal_commit} -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%{_bindir}/astal
%{_libdir}/girepository-1.0/AstalIO-0.1.typelib
%{_libdir}/libastal-io.so.0{,.*}

%files devel
%{_datadir}/gir-1.0/AstalIO-0.1.gir
%{_datadir}/vala/vapi/astal-io-0.1.vapi
%{_includedir}/astal-io.h
%{_libdir}/libastal-io.so
%{_libdir}/pkgconfig/astal-io-0.1.pc

%changelog
%autochangelog
