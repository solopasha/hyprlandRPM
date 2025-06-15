%global commit0 9d4963e7394485ba4735779519c59275901de6ab
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 66

Name:           hyprland-contrib
Version:        0.1%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        %autorelease
Summary:        Community scripts and utilities for Hypr projects
BuildArch:      noarch

License:        MIT
URL:            https://github.com/hyprwm/contrib
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  make
BuildRequires:  scdoc

Recommends:     try_swap_workspace
Recommends:     shellevents
Recommends:     scratchpad
Recommends:     hyprprop
Recommends:     grimblast
Recommends:     hdrop

%description
%{summary}.

%package -n grimblast
Summary:        A helper for screenshots within hyprland
Requires:       grim slurp wl-clipboard jq /usr/bin/notify-send hyprpicker

%description -n grimblast
%{summary}.

%files -n grimblast
%{_bindir}/grimblast
%{_mandir}/man1/grimblast.1.*


%package -n hyprprop
Summary:        An xprop replacement for hyprland
Requires:       slurp jq

%description -n hyprprop
%{summary}.

%files -n hyprprop
%{_bindir}/hyprprop
%{_mandir}/man1/hyprprop.1.*


%package -n scratchpad
Summary:        Send focused window to a special workspace named scratchpad
Requires:       jq
Recommends:     /usr/bin/notify-send

%description -n scratchpad
%{summary}.

%files -n scratchpad
%{_bindir}/scratchpad


%package -n shellevents
Summary:        Invoke shell functions in response to hyprland socket2 events
Requires:       socat

%description -n shellevents
%{summary}.

%files -n shellevents
%{_bindir}/shellevents
%{_bindir}/shellevents_default.sh


%package -n try_swap_workspace
Summary:        Move arbitrary workspace to arbritrary monitor and swap workspaces
Recommends:     /usr/bin/notify-send

%description -n try_swap_workspace
%{summary}.

%files -n try_swap_workspace
%{_bindir}/try_swap_workspace


%package -n hdrop
Summary:        This script emulates the main feature of tdrop (https://github.com/noctuid/tdrop) in Hyprland
Requires:       jq
Recommends:     /usr/bin/notify-send

%description -n hdrop
%{summary}.

%files -n hdrop
%{_bindir}/hdrop
%{_mandir}/man1/hdrop.1.*


%prep
%autosetup -n contrib-%{commit0}


%install
for script in grimblast hyprprop scratchpad shellevents try_swap_workspace hdrop
do
pushd $script
%make_install DESTDIR=%{buildroot} PREFIX=%{buildroot}%{_prefix}
popd
done


%files
%license LICENSE
%doc README.md


%changelog
%autochangelog
