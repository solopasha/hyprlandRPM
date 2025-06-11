Name:           hyprland-autoname-workspaces
Version:        1.1.15
Release:        %autorelease -b2
Summary:        Hyprland autoname workspaces

License:        ISC
URL:            https://github.com/hyprland-community/hyprland-autoname-workspaces
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  rust-packaging >= 21
BuildRequires:  systemd-rpm-macros

%description
This app automatically rename workspaces with icons of started
applications - tested with waybar.


%prep
%autosetup -p1
sed '/LICENSE.md$/d' -i Makefile


%build
export RUSTFLAGS="%{build_rustflags}"
make build


%install
%make_install


%files
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service
%{_datadir}/%{name}/


%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%changelog
%autochangelog
