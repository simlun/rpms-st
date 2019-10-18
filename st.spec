Name:             st-simlun
Obsoletes:        st
Provides:         st
Conflicts:        st
Version:          0.8.1
Release:          4.1%{?dist}
Summary:          A simple terminal implementation for X
%global           _stsourcedir %{_usrsrc}/st-user-%{version}-%{release}
License:          MIT
URL:              http://st.suckless.org/
Source0:          http://dl.suckless.org/st/st-%{version}.tar.gz
Source1:          st.desktop
Source2:          st-user
Source3:          st-user.1
Patch0:           base16-solarized-light.diff
BuildRequires:    binutils
BuildRequires:    coreutils
BuildRequires:    gcc
BuildRequires:    desktop-file-utils
BuildRequires:    libX11-devel
BuildRequires:    libXext-devel
BuildRequires:    libXft-devel
BuildRequires:    make
BuildRequires:    sed
Requires:         font(liberationmono)
Requires:         ncurses-base
Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description
A simple virtual terminal emulator for X which sucks less.

%package user
Summary:          Sources and tools for user configuration of st
License:          MIT
Requires:         st-simlun%{?_isa} = %{version}-%{release}
Requires:         binutils
Requires:         coreutils
Requires:         findutils
Requires:         gcc
Requires:         libX11-devel
Requires:         libXext-devel
Requires:         libXft-devel
Requires:         make
Requires:         patch
Requires:         redhat-rpm-config

%description user
Source files for st and a launcher/builder wrapper script for
customized configurations.

%prep
%setup -n st-%{version}
# terminfo entries are provided by ncurses-base
sed -e "/tic .*st.info/d" -i Makefile

%build
CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}" make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}
chmod 755 %{buildroot}%{_prefix}/bin/st
mv %{buildroot}%{_bindir}/st{,-fedora}
install -pm755 %{SOURCE2} %{buildroot}%{_bindir}/st-user
install -Dpm644 %{SOURCE3} %{buildroot}%{_mandir}/man1/st-user.1
for file in \
    %{buildroot}%{_bindir}/st-user \
    %{buildroot}%{_mandir}/man1/st-user.1; do
sed -i -e 's/VERSION/%{version}/' \
       -e 's/RELEASE/%{release}/' \
       ${file}
done
mkdir -p %{buildroot}%{_stsourcedir}
install -m644 config.mk Makefile st.info *.h *.c \
    %{buildroot}%{_stsourcedir}
touch %{buildroot}%{_bindir}/st
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

%pre
[ -L %{_bindir}/st ] || rm -f %{_bindir}/st

%post
%{_sbindir}/update-alternatives --install %{_bindir}/st st \
    %{_bindir}/st-fedora 10

%postun
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove st %{_bindir}/st-fedora
fi

%post user
%{_sbindir}/update-alternatives --install %{_bindir}/st st \
    %{_bindir}/st-user 20

%postun user
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove st %{_bindir}/st-user
fi

%files
%license LICENSE
%doc FAQ LEGACY README TODO st.info
%ghost %{_bindir}/st
%{_bindir}/st-fedora
%{_mandir}/man1/st.*
%{_datadir}/applications/st.desktop

%files user
%ghost %{_bindir}/st
%{_bindir}/st-user
%{_mandir}/man1/st-user.*
%{_stsourcedir}

%changelog
* Fri Oct 18 2019 Simon Lundmark <simon.lundmark@gmail.com> - 0.8.1-4.1
- Configured the base16 Solarized Light color theme

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 10 2018 Petr Šabata <contyk@redhat.com> - 0.8.1-2
- Install all source files for st-user (rhbz#1574165)

* Mon Apr 09 2018 Petr Šabata <contyk@redhat.com> - 0.8.1-1
- 0.8.1 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 12 2016 Petr Šabata <contyk@redhat.com> - 0.7-1
- 0.7 bump
- The user subpackage now properly requires redhat-rpm-config

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 03 2015 Petr Šabata <contyk@redhat.com> - 0.6-3
- Don't own the applications directory (#1249205)

* Thu Jul 09 2015 Petr Šabata <contyk@redhat.com> - 0.6-2
- Discard our terminfo again, it's provided by ncurses-base (#1241615)

* Wed Jul 08 2015 Petr Šabata <contyk@redhat.com> - 0.6-1
- 0.6 bump
- Stop silently discarding our terminfo

* Thu Jun 25 2015 Petr Šabata <contyk@redhat.com> - 0.5-7
- Correct the dep list
- Modernize spec

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Petr Šabata <contyk@redhat.com> - 0.5-4
- Pass command line parameters to respective binaries in st-user (#1129557)

* Thu Jun 26 2014 Petr Šabata <contyk@redhat.com> - 0.5-3
- Introduce the `user' subpackage

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 Petr Šabata <contyk@redhat.com> - 0.5-1
- 0.5 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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
