%global commit0 25da0804b00fffeee17463afd146711b4a05e77b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           hyprlang
Version:        0.2.1^1.git%{shortcommit0}
Release:        %autorelease
Summary:        The official implementation library for the hypr config language

License:        GPL-3.0-or-later
URL:            https://github.com/hyprwm/hyprlang
Source:         %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

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
%{_libdir}/libhyprlang.so.0{,.*}

%files devel
%{_includedir}/hyprlang.hpp
%{_libdir}/libhyprlang.so
%{_libdir}/pkgconfig/hyprlang.pc

%changelog
%autochangelog
