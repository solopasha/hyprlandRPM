%global commit0 6174a2a25f4e216c0f1d0c4278adc23c476b1d09
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 1

Name:           hyprutils
Version:        0.1.5%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        %autorelease
Summary:        Hyprland utilities library used across the ecosystem

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprutils
Source:         %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(pixman-1)

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Development files for %{name}.

%prep
%autosetup -n %{name}-%{commit0} -p1

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
%{_libdir}/lib%{name}.so.%{lua: print((macros.version:gsub('[%^~].*', '')))}
%{_libdir}/lib%{name}.so.0

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
%autochangelog
