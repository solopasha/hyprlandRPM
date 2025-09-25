Name:           pyprland
Version:        2.4.7
Release:        %autorelease -b4
Summary:        Hyprland extensions made easy

License:        MIT
URL:            https://github.com/hyprland-community/pyprland
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  python3-devel

%description
Pyprland is a host process for multiple Hyprland extensions, aiming at
simplicity and efficiency.
It provides a variety of plugins you can enable to your liking.

%prep
%autosetup -p1
find -type f -exec sed -i '1s|^#!/bin/env python$|#!%{python3}|' {} +

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel
pushd client
gcc %{build_cflags} %{build_ldflags} -o pypr-client pypr-client.c

%install
%pyproject_install
%pyproject_save_files pyprland
install -Dpm0755 client/pypr-client -t %{buildroot}%{_bindir}

%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/pypr
%{_bindir}/pypr-client

%changelog
%autochangelog
