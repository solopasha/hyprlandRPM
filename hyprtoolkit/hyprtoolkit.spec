%global commit0 47524bdfbef76700f2ea1b89f1d08e2b02fc1c63
%global shortcommit0 %{sub %{commit0} 1 7}
%global bumpver 1

Name:           hyprtoolkit
Version:        0.1.0%{?bumpver:~%{bumpver}.git%{shortcommit0}}
Release:        %autorelease
Summary:        A modern C++ Wayland-native GUI toolkit

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprtoolkit
Source:         %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  cmake(hyprwayland-scanner)
BuildRequires:  gcc-c++
BuildRequires:  mesa-libEGL-devel
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aquamarine)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig(aquamarine)
Requires:       pkgconfig(cairo)
Requires:       pkgconfig(hyprgraphics)
%description    devel
Development files for %{name}.

%prep
%autosetup -n %{name}-%{commit0} -p1


%build
%cmake -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprtoolkit.so.0.1.0
%{_libdir}/libhyprtoolkit.so.1

%files devel
%{_includedir}/hyprtoolkit/
%{_libdir}/libhyprtoolkit.so
%{_libdir}/pkgconfig/hyprtoolkit.pc

%changelog
%autochangelog
