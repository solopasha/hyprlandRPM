%global astal_commit 7f2292f0792ffc9b127d4788b3dd3f104b5374b2
%global astal_shortcommit %(c=%{astal_commit}; echo ${c:0:7})
%global bumpver 11

%global debug_package %{nil}
%global _vpath_srcdir lang/gjs

Name:           astal-gjs
Version:        0~%{bumpver}.git%{astal_shortcommit}
Release:        %autorelease
Summary:        Astal GJS pacakge

License:        LGPL-2.1-only
URL:            https://github.com/Aylur/astal
Source0:        %{url}/archive/%{astal_commit}/%{name}-%{astal_shortcommit}.tar.gz

BuildRequires:  meson
BuildRequires:  pkgconfig(astal-io-0.1)
BuildRequires:  pkgconfig(astal-3.0)

Requires:       gjs%{?_isa}
Requires:       astal-io%{?_isa}
Requires:       astal%{?_isa}

Supplements:    astal

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
%dir %{_datadir}/astal
%{_datadir}/astal/gjs/

%files devel
%{_libdir}/pkgconfig/%{name}.pc

%changelog
%autochangelog
