Name:           hyprsunset
Version:        0.3.3
Release:        %autorelease -b2
Summary:        An application to enable a blue-light filter on Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprsunset
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

%description
%{summary}.

%prep
%autosetup -p1

%build
%cmake -DCMAKE_BUILD_TYPE=Release
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
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service

%changelog
%autochangelog
