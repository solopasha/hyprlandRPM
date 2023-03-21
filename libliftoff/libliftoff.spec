Name:           libliftoff
Version:        0.4.1
Release:        1%{?dist}
Summary:        Lightweight KMS plane library

License:        MIT
URL:            https://gitlab.freedesktop.org/emersion/libliftoff
Source0:        %{url}/-/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires:  meson >= 0.52.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig(libdrm)

%description
libliftoff eases the use of KMS planes from userspace without
standing in your way. Users create "virtual planes" called
layers, set KMS properties on them, and libliftoff will
allocate planes for these layers if possible.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n %{name}-v%{version}


%build
%meson
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md
%{_libdir}/*.so.0*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 19 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 0.3.0-1
- Rebase to version 0.3.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Feb 10 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.2.0-1
- Rebase to version 0.2.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 04 2021 Neal Gompa <ngompa13@gmail.com> - 0.1.0-1
- Rebase to version 0.1.0

* Wed Apr 07 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.0.0~git20201110.24abeb9-1
- Update to git snapshot required for gamescope 3.7.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git20201031.0095702-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov  3 13:38:26 EST 2020 Neal Gompa <ngompa13@gmail.com> - 0.0.0~git20201031.0095702-1
- Update to new git snapshot

* Sun Oct  4 15:05:36 EDT 2020 Neal Gompa <ngompa13@gmail.com> - 0.0.0~git20200526.b004282-1
- Initial packaging
