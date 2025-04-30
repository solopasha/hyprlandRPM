Name:           hyprland-qtutils
Version:        0.1.4
Release:        %autorelease -b2
Summary:        Hyprland Qt/qml utility apps
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-qtutils
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel

BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  wayland-devel

Requires:       hyprland-qt-support%{?_isa}

%description
%{summary}.

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
%{_bindir}/hyprland-dialog
%{_bindir}/hyprland-donate-screen
%{_bindir}/hyprland-update-screen

%changelog
%autochangelog
