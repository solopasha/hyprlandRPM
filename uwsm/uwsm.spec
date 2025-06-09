Name:           uwsm
Version:        0.21.8
Release:        %autorelease
Summary:        Universal Wayland Session Manager

License:        MIT
URL:            https://github.com/Vladimir-csp/uwsm
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  meson
BuildRequires:  python-rpm-macros
BuildRequires:  python3
BuildRequires:  python3-dbus
BuildRequires:  python3-pyxdg
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros

Requires:       python3
Requires:       python3-dbus
Requires:       python3-pyxdg
Requires:       util-linux

Recommends:     /usr/bin/notify-send
Recommends:     /usr/bin/whiptail
Recommends:     wofi

%description
Wraps standalone Wayland compositors into a set of Systemd units on the fly.
This provides robust session management including environment, XDG autostart
support, bi-directional binding with login session, and clean shutdown.
For compositors this is an opportunity to offload Systemd integration and
session/XDG autostart management in Systemd-managed environments.

%prep
%autosetup -p1

%build
%meson -Duuctl=enabled -Dfumon=enabled -Duwsm-app=enabled
%meson_build

%install
%meson_install
%py_byte_compile %{python3} %{buildroot}%{_datadir}/%{name}/modules

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post
%systemd_user_post fumon.service

%preun
%systemd_user_preun fumon.service

%postun
%systemd_user_postun fumon.service

%files
%doc %{_docdir}/%{name}/
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-app
%{_bindir}/%{name}-terminal
%{_bindir}/%{name}-terminal-scope
%{_bindir}/%{name}-terminal-service
%{_bindir}/fumon
%{_bindir}/uuctl
%{_datadir}/%{name}/
%{_datadir}/applications/uuctl.desktop
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/fumon.1.*
%{_mandir}/man1/uuctl.1.*
%{_mandir}/man1/uwsm-app.1.*
%{_mandir}/man3/%{name}-plugins.3.*
%{_userunitdir}/fumon.service

%changelog
%autochangelog
