%global sdbus_version 1.5.0

Name:           hypridle
Version:        0.1.2
Release:        %autorelease
Summary:        Hyprland's idle daemon
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hypridle
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/Kistler-Group/sdbus-cpp/archive/v%{sdbus_version}/sdbus-%{sdbus_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
%if %{fedora} >= 40
BuildRequires:  pkgconfig(sdbus-c++)
%else
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
%endif

%description
%{summary}.


%prep
%autosetup
%if %{fedora} < 40
%autosetup -NDT -a1
%endif

%build
%if %{fedora} < 40
pushd sdbus-cpp-%{sdbus_version}
%cmake \
    -DCMAKE_INSTALL_PREFIX=%{_builddir}/sdbus \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF
%cmake_build
cmake --install %{__cmake_builddir}
popd
export PKG_CONFIG_PATH=%{_builddir}/sdbus/lib64/pkgconfig
%endif
%cmake
%cmake_build


%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun %{name}.service


%changelog
%autochangelog
