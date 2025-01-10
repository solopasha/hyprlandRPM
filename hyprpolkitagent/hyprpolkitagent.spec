Name:           hyprpolkitagent
Version:        0.1.2
Release:        %autorelease
Summary:        A simple polkit authentication agent for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpolkitagent
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros

BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-qt6-1)

Requires:       hyprland-qt-support%{?_isa}

%description
A simple polkit authentication agent for Hyprland, written in QT/QML.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%doc README.md
%{_datadir}/dbus-1/services/%{name}.service
%{_libexecdir}/%{name}
%{_userunitdir}/%{name}.service

%changelog
%autochangelog
