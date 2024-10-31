Name:           nwg-clipman
Version:        0.2.4
Release:        %autorelease
Summary:        GTK3-based GUI for cliphist

License:        MIT
URL:            https://github.com/nwg-piotr/nwg-clipman
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       cliphist
Requires:       gtk-layer-shell
Requires:       python3-gobject

%description
%{summary}.

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/nwg_clipman/
%{python3_sitelib}/nwg_clipman-*.egg-info/

%changelog
%autochangelog
