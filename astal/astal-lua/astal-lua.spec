%global astal_commit ee91402cabc994bb4fb7c3f5405a218ad0b57fd3
%global astal_shortcommit %(c=%{astal_commit}; echo ${c:0:7})
%global bumpver 4

%global debug_package %{nil}
%global _vpath_srcdir lang/lua

Name:           astal-lua
Version:        0~%{bumpver}.git%{astal_shortcommit}
Release:        %autorelease
Summary:        Lua bindings for libastal

License:        LGPL-2.1-only
URL:            https://github.com/Aylur/astal
Source0:        %{url}/archive/%{astal_commit}/%{name}-%{astal_shortcommit}.tar.gz
BuildArch:      noarch

BuildRequires:  lua-devel

Requires:       astal
Requires:       astal-io
Requires:       lua-lgi
%{?lua_requires}

%description
%{summary}.

%prep
%autosetup -n astal-%{astal_commit} -p1

%build

%install
pushd %{_vpath_srcdir}
mkdir -p %{buildroot}%{lua_pkgdir}
cp -pr astal %{buildroot}%{lua_pkgdir}

%files
%license LICENSE
%{lua_pkgdir}/astal/

%changelog
%autochangelog
