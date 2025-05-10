Name:           mpvpaper
Version:        1.8
Release:        %autorelease
Summary:        A video wallpaper program

License:        GPL-3.0-or-later
URL:            https://github.com/GhostNaN/mpvpaper
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(mpv)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)

%description
mpvpaper is a wallpaper program for wlroots based wayland compositors,
such as sway. That allows you to play videos with mpv as your wallpaper.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

install -Dpm0644 %{name}.man %{buildroot}/%{_mandir}/man1/%{name}.1

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-holder
%{_mandir}/man1/%{name}.1.*

%changelog
%autochangelog
