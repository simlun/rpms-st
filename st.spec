Name:           st
Version:        0.4.1
Release:        1%{?dist}
Summary:        A simple terminal implementation for X
Group:          User Interface/X
License:        MIT
URL:            http://%{name}.suckless.org/
Source0:        http://dl.suckless.org/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Patch0:         %{name}-0.4-optflags.patch
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXft-devel
BuildRequires:  ncurses
BuildRequires:  desktop-file-utils
Requires:       font(liberationmono)

%description
A simple virtual terminal emulator for X which sucks less.

%prep
%setup -q
%patch0 -p1

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_datadir}/terminfo/s
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

%files
%doc LICENSE README TODO st.info
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/applications

%changelog
* Tue Apr 23 2013 Petr Šabata <contyk@redhat.com> - 0.4.1-1
- 0.4.1 bump

* Tue Apr 02 2013 Petr Šabata <contyk@redhat.com> - 0.4-1
- 0.4 bump
- License change to MIT
- Switching back to Xinerama
- Include terminfo in doc so users can build it themselves if needed

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Petr Šabata <contyk@redhat.com> - 0.3-1
- 0.3 bump
- Switch to Xft
- Our terminfo should now be a part of ncurses; do not require ncurses-term
- Update source URL

* Thu Oct 04 2012 Petr Šabata <contyk@redhat.com> - 0.2.1-6
- Remove the obsolete conflict with openstack-swift (#857891)

* Mon Aug 06 2012 Petr Šabata <contyk@redhat.com> - 0.2.1-5
- Include the latest upstream features

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 29 2012 Petr Šabata <contyk@redhat.com> - 0.2.1-3
- Correct the ncurses-term dependency

* Mon Feb 27 2012 Petr Šabata <contyk@redhat.com> - 0.2.1-2
- Do not install terminfo entries since those are already included in the
  ncurses package (#797828)

* Thu Feb 16 2012 Petr Šabata <contyk@redhat.com> - 0.2.1-1
- 0.2.1 bump

* Wed Feb 08 2012 Petr Šabata <contyk@redhat.com> - 0.2-1
- 0.2 bump
- Drop defattr

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for glibc bug#747377

* Mon May 23 2011 Petr Sabata <psabata@redhat.com> - 0.1.1-2
- We have a conflict with openstack-swift (#693363)

* Mon Apr  4 2011 Petr Sabata <psabata@redhat.com> - 0.1.1-1
- Initial import
