%global sdbus_version 2.1.0

Name:           hyprlock
Version:        0.8.2
Release:        %autorelease
Summary:        Hyprland's GPU-accelerated screen locking utility
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprlock
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source:         https://github.com/Kistler-Group/sdbus-cpp/archive/v%{sdbus_version}/sdbus-%{sdbus_version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  cmake(hyprwayland-scanner)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(opengl)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

Provides:       bundled(sdbus-cpp) = %{sdbus_version}

%description
%{summary}.

%prep
%autosetup -p1
mkdir -p subprojects/sdbus-cpp
tar -xf %{SOURCE1} -C subprojects/sdbus-cpp --strip=1

%build
pushd subprojects/sdbus-cpp
%cmake \
    -DCMAKE_INSTALL_PREFIX=%{_builddir}/sdbus \
    -DCMAKE_BUILD_TYPE=Release \
    -DSDBUSCPP_BUILD_DOCS=OFF \
    -DBUILD_SHARED_LIBS=OFF
%cmake_build
cmake --install %{_vpath_builddir}
popd
export PKG_CONFIG_PATH=%{_builddir}/sdbus/%{_lib}/pkgconfig

%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install
rm %{buildroot}%{_datadir}/hypr/%{name}.conf

%files
%license LICENSE
%doc README.md assets/example.conf
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}

%changelog
%autochangelog
