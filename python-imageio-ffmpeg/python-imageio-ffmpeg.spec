Name:           python-imageio-ffmpeg
Version:        0.6.0
Release:        %autorelease -b4
Summary:        FFMPEG wrapper for Python

License:        BSD-2-Clause
URL:            https://github.com/imageio/imageio-ffmpeg
Source:         %{url}/archive/v%{version}/screeninfo-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%global _description %{expand:
FFMPEG wrapper for Python.}

%description %_description

%package -n python3-imageio-ffmpeg
Summary:        %{summary}
Requires:       /usr/bin/ffmpeg

%description -n python3-imageio-ffmpeg %_description

%prep
%autosetup -p1 -n imageio-ffmpeg-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-imageio-ffmpeg
%doc README.md
%license LICENSE
%{python3_sitelib}/imageio_ffmpeg-*.egg-info/
%{python3_sitelib}/imageio_ffmpeg/

%changelog
%autochangelog
