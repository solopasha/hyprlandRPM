Name:           hyprlauncher
Version:        0.1.1
Release:        %autorelease
Summary:        A multipurpose and versatile launcher / picker for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprlauncher
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprtoolkit)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwire)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libqalculate)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)

Requires:       wl-clipboard

%description
%{summary}.

%prep
%autosetup -p1

%build
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
%autochangelog
