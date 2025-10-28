Name:           hyprtoolkit
Version:        0.2.0
Release:        %autorelease
Summary:        A modern C++ Wayland-native GUI toolkit

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprtoolkit
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  cmake(hyprwayland-scanner)
BuildRequires:  gcc-c++
BuildRequires:  mesa-libEGL-devel
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aquamarine)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig(aquamarine)
Requires:       pkgconfig(cairo)
Requires:       pkgconfig(hyprgraphics)
%description    devel
Development files for %{name}.

%prep
%autosetup -p1

%build
%cmake -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.%{version}
%{_libdir}/lib%{name}.so.2

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
%autochangelog
