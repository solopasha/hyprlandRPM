%global commit0 00beba904fa73f8e0f582c9a9e9679e7bda77e23
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 2

Name:           hyprsysteminfo
Version:        0~%{bumpver}.git%{shortcommit0}
Release:        %autorelease
Summary:        An application to display information about the running system
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprsysteminfo
Source:         %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++

BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(hyprutils)

Requires:       /usr/bin/lscpu
Requires:       /usr/bin/lspci
Requires:       /usr/bin/free
Requires:       kf6-qqc2-desktop-style%{?_isa}

%description
A tiny qt6/qml application to display information about the running system,
or copy diagnostics data, without the terminal.

%prep
%autosetup -n %{name}-%{commit0} -p1

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
