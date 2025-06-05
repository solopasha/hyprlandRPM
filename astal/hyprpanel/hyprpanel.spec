%global commit0 20532ee760fdf492afcf987ae091497a37878197
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 9

%global debug_package %{nil}

Name:           hyprpanel
Version:        0~%{bumpver}.git%{shortcommit0}
Release:        %autorelease
Summary:        A panel built for Hyprland with Astal

License:        MIT
URL:            https://github.com/Jas-SinghFSU/HyprPanel
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  /usr/bin/sass
BuildRequires:  aylurs-gtk-shell2
BuildRequires:  meson

Requires:       /usr/bin/bluetoothctl
Requires:       /usr/bin/sass
Requires:       /usr/bin/wireplumber
Requires:       /usr/bin/wl-copy
Requires:       /usr/bin/wl-paste
Requires:       aylurs-gtk-shell2
Requires:       bluez
Requires:       gnome-bluetooth
Requires:       gtksourceview3
Requires:       gvfs
Requires:       libgtop2
Requires:       libsoup3
Requires:       NetworkManager
Requires:       upower

Recommends:     ppd-service
%if 0%{?fedora} && 0%{?fedora} < 41
Suggests:       power-profiles-daemon
%else
Suggests:       tuned-ppd
%endif
Recommends:     brightnessctl
Recommends:     btop
Recommends:     grimblast
Recommends:     hypridle
Recommends:     hyprpicker
Recommends:     hyprsunset
Recommends:     jq
Recommends:     matugen
Recommends:     swww
Recommends:     wf-recorder

Provides:       HyprPanel

%description
%{summary}.

%prep
%autosetup -n HyprPanel-%{commit0} -p1

%build
%meson
%meson_build

%install
%meson_install
mkdir -p %{buildroot}%{_fontbasedir}
mv %{buildroot}%{_datadir}/%{name}/assets/fonts %{buildroot}%{_fontbasedir}/nf-hyprpanel

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_fontbasedir}/nf-hyprpanel/

%changelog
%autochangelog
