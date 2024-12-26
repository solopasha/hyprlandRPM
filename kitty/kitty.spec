%global forgeurl https://github.com/kovidgoyal/kitty
%global commit0 e9c4e73103ac52cb170cf157803b54381a332203
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global bumpver 1

%define go_vendor_archive %{lua: print("vendor-"..(macros.bumpver and macros.shortcommit0 or macros.version)..".tar.gz")}

%bcond test 1
%bcond bundled 1

%if %{with bundled}
%global gomodulesmode GO111MODULE=on
%endif

%global goipath kitty

Name:           kitty
Version:        0.38.1%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        %autorelease
Summary:        Cross-platform, fast, feature full, GPU based terminal emulator

# GPL-3.0-only: kitty
# Zlib: glfw
# LGPL-2.1-or-later: kitty/iqsort.h
# MIT: docs/_static/custom.css, shell-integration/ssh/bootstrap-utils.sh
# MIT AND CC0-1.0: simde
# CC0-1.0: c-ringbuf
# BSD-2-Clause: base64simd
# MIT: NerdFontsSymbolsOnly
# Go dependencies:
# github.com/alecthomas/chroma: MIT
# github.com/ALTree/bigfloat: MIT
# github.com/bmatcuk/doublestar: MIT
# github.com/disintegration/imaging: MIT
# github.com/dlclark/regexp2: MIT
# github.com/google/go-cmp/cmp: BSD-3-Clause
# github.com/google/uuid: BSD-3-Clause
# github.com/klauspost/cpuid: MIT
# github.com/go-ole/go-ole: MIT
# github.com/lufia/plan9stats: BSD-3-Clause
# github.com/power-devops/perfstat: MIT
# github.com/seancfoley/bintree: Apache-2.0
# github.com/seancfoley/ipaddress-go/ipaddr: Apache-2.0
# github.com/shirou/gopsutil: BSD-3-Clause
# github.com/shoenig/go-m1cpu: MPL-2.0
# github.com/tklauser/go-sysconf: BSD-3-Clause
# github.com/tklauser/numcpus: Apache-2.0
# github.com/zeebo/xxh3: BSD-2-Clause
# golang.org/x/exp: BSD-3-Clause
# golang.org/x/image: BSD-3-Clause
# golang.org/x/sys: BSD-3-Clause
# howett.net/plist: BSD-2-Clause AND BSD-3-Clause
License:        GPL-3.0-only AND LGPL-2.1-or-later AND Zlib AND (MIT AND CC0-1.0) AND BSD-2-Clause AND CC0-1.0
URL:            https://github.com/kovidgoyal/kitty
%if 0%{?bumpver}
Source0:        https://github.com/kovidgoyal/kitty/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
%else
Source0:        https://github.com/kovidgoyal/kitty/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source4:        https://github.com/kovidgoyal/kitty/releases/download/v%{version}/%{name}-%{version}.tar.xz.sig
Source5:        https://calibre-ebook.com/signatures/kovid.gpg
%endif
# bash bundle_go_deps_for_rpm.sh kitty.spec
%if ! 0%{?epel}
Source6:        %{go_vendor_archive}
%else
Source6:        vendor-%{version}.tar.gz
%endif
# Add AppData manifest file
# * https://github.com/kovidgoyal/kitty/pull/2088
Source1:        https://raw.githubusercontent.com/kovidgoyal/kitty/46c0951751444e4f4994008f0d2dcb41e49389f4/kitty/data/%{name}.appdata.xml

Source2:        https://github.com/ryanoasis/nerd-fonts/releases/latest/download/NerdFontsSymbolsOnly.tar.xz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  golang >= 1.22.0
BuildRequires:  go-rpm-macros
BuildRequires:  git-core

BuildRequires:  gnupg2
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  go-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  lcms2-devel
BuildRequires:  libappstream-glib
BuildRequires:  ncurses
BuildRequires:  wayland-devel
BuildRequires:  simde-static

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

%if %{with test}
# For tests:
BuildRequires:  fish
BuildRequires:  glibc-common
%if 0%{?epel}
BuildRequires:  glibc-langpack-en
%endif
BuildRequires:  openssh-clients
BuildRequires:  python3dist(pillow)
BuildRequires:  ripgrep
BuildRequires:  zsh
%endif

Requires:       python3%{?_isa}
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
Requires:       %{name}-kitten%{?_isa} = %{version}-%{release}

# For the "Hyperlinked grep" feature
Recommends:     ripgrep

# Very weak dependencies, these are required to enable all features of kitty's
# "kittens" functions install separately
Suggests:       ImageMagick%{?_isa}

Provides:       bundled(font(SymbolsNFM))

Provides:       bundled(Verstable) = 2.1.1
# modified version of https://github.com/dhess/c-ringbuf
Provides:       bundled(c-ringbuf)
# heavily modified
Provides:       bundled(glfw)
# https://github.com/aklomp/base64
Provides:       bundled(base64simd)

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
License:        GPL-3.0-only
BuildArch:      noarch

Requires:       ncurses-base

%description    terminfo
Cross-platform, fast, feature full, GPU based terminal emulator.

The terminfo file for Kitty Terminal.

# shell-integration package
%package        shell-integration
Summary:        Shell integration scripts for %{name}
License:        GPL-3.0-only AND MIT
BuildArch:      noarch

Recommends:     %{name}-kitten

%description    shell-integration
%{summary}.

# kitten package
%package        kitten
Summary:        The kitten executable
License:        GPL-3.0-only AND MIT AND BSD-3-Clause AND BSD-2-Clause AND Apache-2.0 AND MPL-2.0 AND (BSD-2-Clause AND BSD-3-Clause)

%description    kitten
%{summary}.

# doc package
%package        doc
Summary:        Documentation for %{name}
License:        GPL-3.0-only AND MIT
BuildArch:      noarch

BuildRequires:  python3dist(sphinx)
%if ! 0%{?epel}
BuildRequires:  python3dist(sphinx-copybutton)
BuildRequires:  python3dist(sphinx-inline-tabs)
BuildRequires:  python3dist(sphinxext-opengraph)
%endif

%description    doc
This package contains the documentation for %{name}.


%prep
%if ! 0%{?bumpver}
%{gpgverify} --keyring='%{SOURCE5}' --signature='%{SOURCE4}' --data='%{SOURCE0}'
%endif
%autosetup -p1 %{?bumpver:-n %{name}-%{commit0}} %{?with_bundled:-a6}
mkdir fonts
tar -xf %{SOURCE2} -C fonts

# Changing sphinx theme to classic
sed "s/html_theme = 'furo'/html_theme = 'classic'/" -i docs/conf.py

# Replace python shebangs to make them compatible with fedora
find -type f -name "*.py" -exec sed -e 's|/usr/bin/env python3|%{python3}|g'    \
                                    -e 's|/usr/bin/env python|%{python3}|g'     \
                                    -e 's|/usr/bin/env -S kitty|/usr/bin/kitty|g' \
                                    -i "{}" \;

mkdir src
ln -s ../ src/kitty

%if 0%{?epel}
sed '1i \#define XKB_KEY_XF86Fn 0x100811d0' -i kitty/keys.c
%endif

%if %{without bundled}
%generate_buildrequires
export GOPATH=$(pwd):%{gopath}
%go_generate_buildrequires
%endif

%build
%set_build_flags
%{python3} setup.py linux-package   \
    --libdir-name=%{_lib}           \
    --update-check-interval=0       \
    --skip-building-kitten          \
    --verbose                       \
    --ignore-compiler-warnings

%if %{without bundled}
export GOPATH=$(pwd):%{gopath}
%endif
unset LDFLAGS
mkdir -p _build/bin
%gobuild -o _build/bin/kitten %{?with_bundled:./tools/cmd}%{!?with_bundled:./src/kitty/tools/cmd}

%if 0%{?bumpver}
ln -sr _build/bin/kitten kitty/launcher/
make docs
%endif


%install
# rpmlint fixes
find linux-package -type f ! -executable -name "*.py" -exec sed -i '1{\@^#!%{python3}@d}' "{}" \;
find linux-package/%{_lib}/%{name}/shell-integration -type f ! -executable -exec sed -r -i '1{\@^#!/bin/(fish|zsh|sh|bash)@d}' "{}" \;

cp -r linux-package %{buildroot}%{_prefix}
install -m0755 -Dp _build/bin/kitten %{buildroot}%{_bindir}/kitten

install -m0644 -Dp %{SOURCE1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%if 0%{?bumpver}
install -m 0755 -vd %{buildroot}%{_mandir}/man{1,5}
install -m 0644 -p docs/_build/man/*.1 %{buildroot}%{_mandir}/man1
install -m 0644 -p docs/_build/man/*.5 %{buildroot}%{_mandir}/man5
install -m 0755 -vd %{buildroot}%{_docdir}/%{name}
cp -r docs/_build/html %{buildroot}%{_docdir}/%{name}
%endif

# rpmlint fixes
rm %{buildroot}%{_datadir}/doc/%{name}/html/.buildinfo \
   %{buildroot}%{_datadir}/doc/%{name}/html/.nojekyll


%check
%if %{with test}
sed '/def test_ssh_shell_integration/a \
\        self.skipTest("Skipping a flaky test")' -i kitty_tests/ssh.py
%if 0%{?epel}
sed '/def test_ssh_leading_data/a \
\        self.skipTest("Skipping a failing test")' -i kitty_tests/ssh.py

for test in "TestRgArgParsing" \
; do
awk -i inplace '/^func.*'"$test"'\(/ { print; print "\tt.Skip(\"disabled failing test\")"; next}1' $(grep -rl $test)
done
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
%endif
%ifarch ppc64le
for test in test_transfer_receive test_transfer_send; do
sed "/def $test/a \
\        self.skipTest(\"Skipping a failing test\")" -i kitty_tests/file_transmission.py
done
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
%{python3} setup.py test          \
    --prefix=%{buildroot}%{_prefix}
%endif

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop


%files
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.{png,svg}
%{_libdir}/%{name}/
%exclude %{_libdir}/%{name}/shell-integration
%{_mandir}/man{1,5}/*.{1,5}*
%{_metainfodir}/*.xml

%files kitten
%if %{with bundled}
# Go bundled provides generator
%license vendor/modules.txt
%endif
%license LICENSE
%{_bindir}/kitten

%files terminfo
%license LICENSE
%{_datadir}/terminfo/x/xterm-%{name}

%files shell-integration
%license LICENSE
%{_libdir}/%{name}/shell-integration/

%files doc
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.rst INSTALL.md
%{_docdir}/%{name}/html
%dir %{_docdir}/%{name}


%changelog
%autochangelog
