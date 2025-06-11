%global program_name swaylock

Name:           swaylock-effects
Version:        1.7.0.0
Release:        %autorelease -b2
Summary:        Swaylock, with fancy effects

License:        MIT
URL:            https://github.com/jirutka/swaylock-effects
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  scdoc

Conflicts:      %{program_name}
Provides:       %{program_name}
Provides:       %{program_name}%{?_isa}

%description
Swaylock-effects is a fork of swaylock which adds built-in screenshots and
image manipulation effects like blurring. It's inspired by i3lock-color,
although the feature sets aren't perfectly overlapping.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/pam.d/%{program_name}
%{_bindir}/%{program_name}
%{_mandir}/man1/%{program_name}.1*
%{bash_completions_dir}/%{program_name}
%{fish_completions_dir}/%{program_name}.fish
%{zsh_completions_dir}/_%{program_name}

%changelog
%autochangelog
