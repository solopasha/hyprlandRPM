Name:           waypaper
Version:        2.7
Release:        %autorelease
Summary:        GUI wallpaper setter for Wayland

License:        GPL-3.0-or-later
URL:            https://github.com/anufrievroman/waypaper
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel

Recommends:     swww

%description
GUI wallpaper setter for Wayland and Xorg window managers. It works as
a frontend for popular wallpaper backends like swaybg, swww, wallutils and feh.

%prep
%autosetup -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files waypaper

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/waypaper
%{_datadir}/applications/waypaper.desktop
%{_datadir}/icons/hicolor/scalable/apps/waypaper.svg
%{_datadir}/man/man1/waypaper.1.*

%changelog
%autochangelog
