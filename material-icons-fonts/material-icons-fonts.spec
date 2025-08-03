%global commit0 b2c0f61d8a99224bd99924f3d0471d9f146c9a54
%global shortcommit0 %{sub %{commit0} 1 7}
%global bumpver 1

Version:        4.0.0%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        %autorelease
URL:            https://google.github.io/material-design-icons/

%global fontlicense     Apache-2.0
%global fontlicenses    LICENSE
%global fontdocs        README.md
%global fontfamily      Material Icons
%global fontsummary     Google material design system icons
%global fonts           font/*.otf font/*.ttf variablefont/*.ttf
%global fontorg         com.google
%global fontconfs       %{SOURCE1}

%global fontdescription %{expand:
Material design icons is the official icon set from Google.  The icons
are designed under the material design guidelines.}

Source1:        65-%{fontpkgname}.conf

BuildRequires:  git-core

%fontpkg

%prep
%setup -c
git clone --single-branch --branch=master --filter=blob:none --sparse --depth=1 https://github.com/google/material-design-icons.git .
git sparse-checkout init --cone
git sparse-checkout set font variablefont
git checkout %{commit0}

%build
%fontbuild

%install
%fontinstall
metainfo=%{buildroot}%{_metainfodir}/%{fontorg}.%{name}.metainfo.xml

# The Fedora font macros generate invalid metainfo; see bz 1943727.
sed -e 's,updatecontact,update_contact,g' \
    -e 's,<!\[CDATA\[\(.*\)\]\]>,\1,' \
    -e 's,<font></font>,<font>Material Icons Outlined Regular</font>\n    <font>Material Icons Round Regular</font>\n    <font>Material Icons Sharp Regular</font>\n    <font>Material Icons Two Tone Regular</font>,' \
    -i $metainfo

%check
%fontcheck

%fontfiles

%changelog
%autochangelog
