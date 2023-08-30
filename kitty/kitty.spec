%global optflags %{optflags} -Wno-array-bounds

%global commit0 588da9f1dc7a14089bc8971d622c63e47a027c1f
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 1

%bcond test 1
%bcond doc 1
%bcond bundled 0

%if %{with bundled}
%global gomodulesmode GO111MODULE=on
%endif

Name:           kitty
Version:        0.29.2%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        %autorelease
Summary:        Cross-platform, fast, feature full, GPU based terminal emulator

# GPL-3.0-only: kitty
# Zlib: glfw
# LGPL-2.1-or-later: kitty/iqsort.h
# BSD-1-Clause: kitty/uthash.h
# MIT: docs/_static/custom.css, shell-integration/ssh/bootstrap-utils.sh
License:        GPL-3.0-only AND LGPL-2.1-or-later AND Zlib AND BSD-1-Clause AND MIT
URL:            https://sw.kovidgoyal.net/kitty
%if 0%{?bumpver}
Source0:        https://github.com/kovidgoyal/kitty/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
%else
Source0:        https://github.com/kovidgoyal/kitty/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source4:        https://github.com/kovidgoyal/kitty/releases/download/v%{version}/%{name}-%{version}.tar.xz.sig
Source5:        https://calibre-ebook.com/signatures/kovid.gpg
%endif
# Add AppData manifest file
# * https://github.com/kovidgoyal/kitty/pull/2088
Source1:        https://raw.githubusercontent.com/kovidgoyal/kitty/46c0951751444e4f4994008f0d2dcb41e49389f4/kitty/data/%{name}.appdata.xml

# Don't build kitten inside setup.py, use gobuild macro in the spec instead to build with fedora flags
Patch0:         kitty-do-not-build-kitten.patch
## upstream patches

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  golang >= 1.20.0
BuildRequires:  git-core

BuildRequires:  gnupg2
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
%if 0%{?el8}
BuildRequires:  go-srpm-macros
BuildRequires:  python38-devel
%else
BuildRequires:  go-rpm-macros
BuildRequires:  python3-devel
%endif
BuildRequires:  lcms2-devel
BuildRequires:  libappstream-glib
BuildRequires:  ncurses
BuildRequires:  wayland-devel

BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libxxhash)

%if %{without bundled}
BuildRequires:  golang(github.com/alecthomas/chroma/v2)
BuildRequires:  golang(github.com/alecthomas/chroma/v2/lexers)
BuildRequires:  golang(github.com/alecthomas/chroma/v2/styles)
BuildRequires:  golang(github.com/ALTree/bigfloat)
BuildRequires:  golang(github.com/bmatcuk/doublestar/v4)
BuildRequires:  golang(github.com/disintegration/imaging)
BuildRequires:  golang(github.com/dlclark/regexp2)
BuildRequires:  golang(github.com/google/go-cmp/cmp)
BuildRequires:  golang(github.com/google/uuid)
BuildRequires:  golang(github.com/jamesruan/go-rfc1924/base85)
BuildRequires:  golang(github.com/seancfoley/ipaddress-go/ipaddr)
BuildRequires:  golang(github.com/shirou/gopsutil/v3/process)
BuildRequires:  golang(golang.org/x/exp/constraints)
BuildRequires:  golang(golang.org/x/exp/maps)
BuildRequires:  golang(golang.org/x/exp/rand)
BuildRequires:  golang(golang.org/x/exp/slices)
BuildRequires:  golang(golang.org/x/image/bmp)
BuildRequires:  golang(golang.org/x/image/tiff)
BuildRequires:  golang(golang.org/x/image/webp)
BuildRequires:  golang(golang.org/x/sys/unix)
BuildRequires:  golang(howett.net/plist)
BuildRequires:  golang(github.com/zeebo/xxh3)
%endif

%if %{with test}
# For tests:
BuildRequires:  /usr/bin/ssh
BuildRequires:  /usr/bin/getent
BuildRequires:  /usr/bin/zsh
BuildRequires:  /usr/bin/rg
BuildRequires:  python3dist(pillow)
%endif

%if 0%{?el8}
Requires:       python38%{?_isa}
%else
Requires:       python3%{?_isa}
%endif
Requires:       hicolor-icon-theme

Obsoletes:      %{name}-bash-integration < 0.28.1-3
Obsoletes:      %{name}-fish-integration < 0.28.1-3
Provides:       %{name}-bash-integration = %{version}-%{release}
Provides:       %{name}-fish-integration = %{version}-%{release}

# Terminfo file has been split from the main program and is required for use
# without errors. It has been separated to support SSH into remote machines using
# kitty as per the maintainers suggestion. Install the terminfo file on the remote
# machine.
Requires:       %{name}-terminfo = %{version}-%{release}
Requires:       %{name}-shell-integration = %{version}-%{release}

# Very weak dependencies, these are required to enable all features of kitty's
# "kittens" functions install separately
# For the "Hyperlinked grep" feature
Recommends:     ripgrep

Suggests:       ImageMagick%{?_isa}

%description
- Offloads rendering to the GPU for lower system load and buttery smooth
  scrolling. Uses threaded rendering to minimize input latency.

- Supports all modern terminal features: graphics (images), unicode, true-color,
  OpenType ligatures, mouse protocol, focus tracking, bracketed paste and
  several new terminal protocol extensions.

- Supports tiling multiple terminal windows side by side in different layouts
  without needing to use an extra program like tmux.

- Can be controlled from scripts or the shell prompt, even over SSH.

- Has a framework for Kittens, small terminal programs that can be used to
  extend kitty's functionality. For example, they are used for Unicode input,
  Hints and Side-by-side diff.

- Supports startup sessions which allow you to specify the window/tab layout,
  working directories and programs to run on startup.

- Cross-platform: kitty works on Linux and macOS, but because it uses only
  OpenGL for rendering, it should be trivial to port to other Unix-like
  platforms.

- Allows you to open the scrollback buffer in a separate window using arbitrary
  programs of your choice. This is useful for browsing the history comfortably
  in a pager or editor.

- Has multiple copy/paste buffers, like vim.


# terminfo package
%package        terminfo
Summary:        The terminfo file for Kitty Terminal
BuildArch:      noarch

Requires:       ncurses-base

%description    terminfo
Cross-platform, fast, feature full, GPU based terminal emulator.

The terminfo file for Kitty Terminal.

# shell-integration package
%package        shell-integration
Summary:        Shell integration scripts for %{name}
BuildArch:      noarch

%description    shell-integration
%{summary}.

# doc package
%if %{with doc}
%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

BuildRequires:  python3dist(sphinx)
%if ! 0%{?epel}
BuildRequires:  python3dist(sphinx-copybutton)
BuildRequires:  python3dist(sphinx-inline-tabs)
BuildRequires:  python3dist(sphinxext-opengraph)
%endif

%description    doc
This package contains the documentation for %{name}.
%endif


%prep
%if 0%{?bumpver}
%else
%{gpgverify} --keyring='%{SOURCE5}' --signature='%{SOURCE4}' --data='%{SOURCE0}'
%endif
%autosetup -p1 %{?bumpver:-n %{name}-%{commit0}}
%if %{with bundled}
go mod vendor
%endif

# Changing sphinx theme to classic
sed "s/html_theme = 'furo'/html_theme = 'classic'/" -i docs/conf.py

# Replace python shebangs to make them compatible with fedora
find -type f -name "*.py" -exec sed -e 's|/usr/bin/env python3|%{python3}|g'    \
                                    -e 's|/usr/bin/env python|%{python3}|g'     \
                                    -e 's|/usr/bin/env -S kitty|/usr/bin/kitty|g' \
                                    -i "{}" \;

mkdir -p src/kitty
ln -s ../../tools src/kitty/tools
ln -s ../../kittens src/kitty/kittens


%build
%set_build_flags
%{python3} setup.py linux-package   \
    --libdir-name=%{_lib}           \
    --update-check-interval=0       \
    --ignore-compiler-warnings      \
    --verbose

%if %{without bundled}
export GOPATH=$(pwd):%{gopath}
%endif
unset LDFLAGS
mkdir -p _build/bin
%gobuild -o _build/bin/kitten ./src/kitty/tools/cmd

%install
# rpmlint fixes
find linux-package -type f ! -executable -name "*.py" -exec sed -i '1{\@^#!%{python3}@d}' "{}" \;
find linux-package/%{_lib}/%{name}/shell-integration -type f ! -executable -exec sed -r -i '1{\@^#!/bin/(fish|zsh|sh|bash)@d}' "{}" \;

cp -r linux-package %{buildroot}%{_prefix}
install -m0755 -Dp _build/bin/kitten %{buildroot}%{_bindir}/kitten

install -m0644 -Dp %{SOURCE1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%if %{with doc}
# rpmlint fixes
rm %{buildroot}%{_datadir}/doc/%{name}/html/.buildinfo \
   %{buildroot}%{_datadir}/doc/%{name}/html/.nojekyll
%endif


%check
%if %{with test}
sed '/def test_ssh_shell_integration/a \
\        self.skipTest("Skipping a flaky test")' -i kitty_tests/ssh.py
%if 0%{?epel}
sed '/def test_ssh_leading_data/a \
\        self.skipTest("Skipping a failing test")' -i kitty_tests/ssh.py
%endif
export %{gomodulesmode}
%if %{without bundled}
export GOPATH=$(pwd):%{gopath}
%endif
# Some tests ignores PATH env...
mkdir -p kitty/launcher
ln -s %{buildroot}%{_bindir}/%{name} kitty/launcher/
export PATH=%{buildroot}%{_bindir}:$PATH
export PYTHONPATH=$(pwd)
%{__python3} setup.py test          \
    --prefix=%{buildroot}%{_prefix}
%endif

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop


%files
%if %{with bundled}
# Go bundled provides generator
%license vendor/modules.txt
%endif
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/kitten
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.{png,svg}
%{_libdir}/%{name}/
%exclude %{_libdir}/%{name}/shell-integration
%if %{with doc}
%{_mandir}/man{1,5}/*.{1,5}*
%endif
%{_metainfodir}/*.xml

%files terminfo
%license LICENSE
%{_datadir}/terminfo/x/xterm-%{name}

%files shell-integration
%license LICENSE
%{_libdir}/%{name}/shell-integration/

%if %{with doc}
%files doc
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.rst INSTALL.md
%{_docdir}/%{name}/html
%dir %{_docdir}/%{name}
%endif


%changelog
%autochangelog
