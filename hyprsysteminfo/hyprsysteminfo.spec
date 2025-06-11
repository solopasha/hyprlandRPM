Name:           hyprsysteminfo
Version:        0.1.3
Release:        %autorelease -b8
Summary:        An application to display information about the running system
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprsysteminfo
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++

BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(hyprutils)

Requires:       /usr/bin/lscpu
Requires:       /usr/bin/lspci
Requires:       /usr/bin/free
Requires:       hyprland-qt-support%{?_isa}

%description
A tiny qt6/qml application to display information about the running system,
or copy diagnostics data, without the terminal.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
%autochangelog
