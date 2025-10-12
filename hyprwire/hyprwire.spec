%global commit0 063d28bf531e50847ac91732a72d94d4ba8fb5df
%global shortcommit0 %{sub %{commit0} 1 7}
%global bumpver 3

Name:           hyprwire
Version:        0.1.0%{?bumpver:~%{bumpver}.git%{shortcommit0}}
Release:        %autorelease
Summary:        A fast and consistent wire protocol for IPC

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwire
Source:         %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libffi)

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Development files for %{name}.

%prep
%autosetup -n %{name}-%{commit0} -p1

%build
%cmake -GNinja \
    -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.0.1.0
%{_libdir}/lib%{name}.so.1

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
%autochangelog
