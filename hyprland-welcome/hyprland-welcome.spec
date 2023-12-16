%global commit0 4c6700bf6edaffb862f357ea0ecfe5db48479ab1
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 3

Name:           hyprland-welcome
Version:        0~%{bumpver}.git%{shortcommit0}
Release:        %autorelease
Summary:        Hyprland's welcome app

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-welcome
Source:         %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake(Qt6Widgets)

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
%{_bindir}/HyprlandWelcome

%changelog
%autochangelog
