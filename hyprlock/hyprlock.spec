%global commit0 5c91621ad2a068793c7844942867ddc297f37c58
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 26

Name:           hyprlock
Version:        0.1.0^%{bumpver}.git%{shortcommit0}
Release:        %autorelease
Summary:        Hyprland's GPU-accelerated screen locking utility
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprlock
Source:         %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(opengl)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

%description
%{summary}.

%prep
%autosetup -n %{name}-%{commit0} -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}

%changelog
%autochangelog
