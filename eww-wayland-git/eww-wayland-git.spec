%global commit0 d96586c209cad2c1098a4caa42133329bef852e8
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 2

Name:           eww-wayland-git
Version:        0.5.0%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        %autorelease
Summary:        ElKowars wacky widgets

License:        MIT
URL:            https://github.com/elkowar/eww
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0)

Provides:       eww
Provides:       eww-wayland

%description
Elkowars Wacky Widgets is a standalone widget system made in Rust that
allows you to implement your own, custom widgets in any window manager.


%prep
%autosetup -n eww-%{commit0}
export RUSTUP_TOOLCHAIN=nightly
curl https://sh.rustup.rs -sSf | sh -s -- --profile minimal -y


%build
export RUSTFLAGS='-Copt-level=3 -Cdebuginfo=1 -Ccodegen-units=1 -Clink-arg=-Wl,-z,relro -Clink-arg=-Wl,-z,now -Clink-arg=-specs=/usr/lib/rpm/redhat/redhat-package-notes'
$HOME/.cargo/bin/cargo build --release --package eww --no-default-features --features wayland


%install
install -Dm755 target/release/eww -t %{buildroot}%{_bindir}


%files
%license LICENSE
%doc examples/ README.md
%{_bindir}/eww


%changelog
%autochangelog
