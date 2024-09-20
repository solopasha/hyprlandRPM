%global portal_commit ca077cc05c370879a6df90eac43a3c2ee6768306
%global portal_shortcommit %(c=%{portal_commit}; echo ${c:0:7})
#global bumpver 1

%global sdbus_version 1.5.0

Name:           xdg-desktop-portal-hyprland
Epoch:          1
Version:        1.3.4%{?bumpver:^%{bumpver}.git%{portal_shortcommit}}
Release:        %autorelease
Summary:        xdg-desktop-portal backend for hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/%{name}
%if 0%{?bumpver}
Source:         %{url}/archive/%{portal_commit}/%{name}-%{version}.tar.gz
%else
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source:         https://github.com/Kistler-Group/sdbus-cpp/archive/v%{sdbus_version}/sdbus-%{sdbus_version}.tar.gz
Patch:          revert-c5b309.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(Qt6Widgets)
%if %{fedora} >= 41
BuildRequires:  pkgconfig(sdbus-c++)
%endif
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(hyprutils)

Requires:       dbus
# required for Screenshot portal implementation
Requires:       grim
Recommends:     hyprpicker
Requires:       xdg-desktop-portal
# required for hyprland-share-picker
Requires:       slurp
Requires:       qt6-qtwayland

Enhances:       hyprland
Supplements:    hyprland
Supplements:    hyprland-legacyrenderer
Supplements:    hyprland-git

%if %{fedora} < 41
Provides:       bundled(sdbus-cpp) = %{sdbus_version}
%endif

%description
%{summary}.


%prep
%autosetup %{?bumpver:-n %{name}-%{portal_commit}} -N
%if %{fedora} < 41
%patch -P 0 -p1
sed -i '/libpipewire/s/>=1.1.82//' CMakeLists.txt
%endif
%if %{fedora} < 41
tar -xf %{SOURCE1} -C subprojects/sdbus-cpp --strip=1
%endif


%build
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF
%cmake_build


%install
%cmake_install


%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service


%files
%license LICENSE
%doc README.md contrib/config.sample
%{_bindir}/hyprland-share-picker
%{_libexecdir}/%{name}
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_datadir}/dbus-1/services/*.service
%{_userunitdir}/%{name}.service


%changelog
%autochangelog
