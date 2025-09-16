Name:           qt6ct-kde
Version:        0.10
Release:        %autorelease -b2
Summary:        Qt6 Configuration Utility, patched to work correctly with KDE applications
License:        BSD-2-Clause
URL:            https://github.com/ilya-fedin/qt6ct
Source:         %{url}/archive/%{version}/qt6ct-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  qt6-rpm-macros
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ColorScheme)
BuildRequires:  cmake(KF6IconThemes)

Requires:       kf6-qqc2-desktop-style%{?_isa}
Requires:       qt6-qtsvg%{?_isa}

Conflicts:      qt6ct
Provides:       qt6ct

%description
This program allows users to configure Qt6 settings (theme, font, icons, etc.)
under DE/WM without Qt integration.

%prep
%autosetup -n qt6ct-%{version} -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%doc AUTHORS README ChangeLog
%license COPYING
%{_bindir}/qt6ct
%{_datadir}/applications/qt6ct.desktop
%{_datadir}/qt6ct/
%{_libdir}/libqt6ct-common.so*
%{_qt6_plugindir}/platformthemes/libqt6ct.so
%{_qt6_plugindir}/styles/libqt6ct-style.so

%changelog
%autochangelog
