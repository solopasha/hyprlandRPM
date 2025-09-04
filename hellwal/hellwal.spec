Name:           hellwal
Version:        1.0.7
Release:        %autorelease
Summary:        Pywal-like color palette generator, but faster and in C

License:        MIT
URL:            https://github.com/danihek/hellwal
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch:          hellwal.patch

BuildRequires:  gcc

%description
%{summary}.

%prep
%autosetup -p1

%build
%make_build hellwal

%install
%make_install
install -Dpm0644 assets/hellwal-completion.bash %{buildroot}%{bash_completions_dir}/%{name}

%files
%license LICENSE
%doc templates
%doc themes
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}

%changelog
%autochangelog
