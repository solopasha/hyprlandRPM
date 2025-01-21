%global debug_package %{nil}

Name:           glaze
Version:        4.3.1
Release:        %autorelease
Summary:        Extremely fast, in memory, JSON and interface library

License:        MIT
URL:            https://github.com/stephenberry/glaze
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch:          fix-path.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
BuildArch:      noarch
Provides:       %{name}-static = %{version}-%{release}
%description    devel
Development files for %{name}.

%prep
%autosetup -p1

%build
%cmake \
    -Dglaze_ENABLE_AVX2:BOOL=OFF \
    -Dglaze_DEVELOPER_MODE:BOOL=OFF \
    -Dglaze_ENABLE_FUZZING:BOOL=OFF
%cmake_build

%install
%cmake_install

%files devel
%license LICENSE
%doc README.md
%{_datadir}/cmake/%{name}/
%{_includedir}/%{name}/

%changelog
%autochangelog
