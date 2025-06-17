%global astal_commit 7f2292f0792ffc9b127d4788b3dd3f104b5374b2
%global astal_shortcommit %(c=%{astal_commit}; echo ${c:0:7})
%global bumpver 7

%bcond bootstrap 0

%global _vpath_srcdir lib/astal/gtk4

Name:           astal-gtk4
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
BuildRequires:  pkgconfig(astal-io-0.1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)

%if %{without bootstrap}
Requires:       astal-libs%{?_isa}
%endif

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
%{_libdir}/girepository-1.0/Astal-4.0.typelib
%{_libdir}/libastal-4.so.4{,.*}

%files devel
%{_datadir}/gir-1.0/Astal-4.0.gir
%{_datadir}/vala/vapi/astal-4-4.0.vapi
%{_includedir}/astal-4.h
%{_libdir}/libastal-4.so
%{_libdir}/pkgconfig/astal-4-4.0.pc

%changelog
%autochangelog
