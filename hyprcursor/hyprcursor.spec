Name:           hyprcursor
Version:        0.1.4
Release:        %autorelease
Summary:        The hyprland cursor format, library and utilities

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprcursor
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libzip)

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

%files
%license LICENSE
%doc README.md
%{_bindir}/hyprcursor-util
%{_libdir}/lib%{name}.so.%{version}
%{_libdir}/lib%{name}.so.0

%files devel
%{_includedir}/%{name}.hpp
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
%autochangelog
