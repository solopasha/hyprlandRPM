%global build_type_safety_c 0

Name:           xcur2png
Version:        0.7.1
Release:        %autorelease
Summary:        Convert X cursors to PNG images

License:        GPL-3.0-or-later
URL:            https://github.com/eworm-de/xcur2png
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Patch:          0001-fix-wrong-math.patch

BuildRequires:  gcc
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(xcursor)

%description
xcur2png is a program which let you take PNG image from X cursor, and generate
config-file which is reusable by xcursorgen. To put it simply, it is
converter from X cursor to PNG image.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*

%changelog
%autochangelog
