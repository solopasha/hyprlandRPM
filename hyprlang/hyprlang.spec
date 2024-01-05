Name:           hyprlang
Version:        0.2.1
Release:        %autorelease -b2
Summary:        The official implementation library for the hypr config language

License:        GPL-3.0-or-later
URL:            https://github.com/hyprwm/hyprlang
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch:          https://github.com/hyprwm/hyprlang/compare/v0.2.1...main.patch
Patch:          libdir.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Development files for %{name}.

%prep
%autosetup -p1


%build
%cmake
%cmake_build


%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprlang.so

%files devel
%{_datadir}/pkgconfig/hyprlang.pc
%{_includedir}/hyprlang.hpp


%changelog
%autochangelog
