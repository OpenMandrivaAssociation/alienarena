Name:		alienarena
Summary:	Multiplayer retro sci-fi deathmatch game
Version:	7.71.4
Release:	1
License:	GPLv2+
Group:		Games/Arcade
# Upstream again tagging new releases but we need to use svn, as example:
# svn checkout svn://svn.icculus.org/alienarena/trunk alienarena
# or
# svn export svn://svn.icculus.org/alienarena/trunk alienarena-7.71.4

Source0:	alienarena-7.71.tar.xz
Source1:	alienarena.desktop
Source2:	GPL.acebot.txt
URL:		https://www.alienarena.org

BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	autoconf
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	desktop-file-utils


Requires:	desktop-file-utils
#Requires:	opengl-games-utils
Requires:	openal

%description
Alien Arena 2011 is an online deathmatch game with over 30 levels, seven modes 
of play, loads of mutators, built-in bots, multiple player characters and weapons
(with alt-fire modes).


%package server
Group:		Games/Arcade
Summary:	Dedicated server for alienarena, the FPS game
Requires:	alienarena-data = 20120106


%description server
Alien Arena 2011 is an online deathmatch game with over 30 levels, seven modes
of play, loads of mutators, built-in bots, multiple player characters and weapons
(with alt-fire modes).

This is the dedicated server.


%prep
%autosetup -p1 -n %{name}-%{version}

# Copy license clarification for acebot
cp -p %{SOURCE2} .

# clean up end-line encoding
[[ -e docs/README.txt ]] && %{__sed} -i 's/\r//' docs/README.txt

# So, AlienArena now "uses" openal by dlopening the library, which is hardcoded to 
# "libopenal.so". That file only lives in openal-devel, so we need to adjust the hardcoding.
LIBOPENAL=`ls %{_libdir}/libopenal.so.? | cut -d "/" -f 4`
%__sed -i "s|\"libopenal.so\"|\"$LIBOPENAL\"|g" source/unix/qal_unix.c

%build
autoreconf -i
export PTHREAD_LIBS="-lpthread"
export PTHREAD_CFLAGS="-pthread"
%configure
%make_build

%install
%make_install

%__mkdir_p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor "%{_real_vendor}"			\
	--dir %{buildroot}%{_datadir}/applications	\
	%{SOURCE1}

%__mkdir_p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
%__mv %{buildroot}%{_datadir}/icons/%{name}.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

# opengl checker
%__ln_s opengl-game-wrapper.sh %{buildroot}%{_bindir}/%{name}-wrapper
%__ln_s crx %{buildroot}%{_bindir}/%{name}
%__ln_s crx-ded %{buildroot}%{_bindir}/%{name}-server

# clean docs as we don't want to package them twice
%__rm -rf %{buildroot}%{_defaultdocdir}/%{name}

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc GPL.acebot.txt COPYING README
%{_bindir}/crx
%{_bindir}/%{name}
%{_bindir}/%{name}-wrapper
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

%files server
%defattr(-,root,root,-)
%{_bindir}/crx-ded
%{_bindir}/%{name}-server



%changelog
* Fri Jan 20 2012 Andrey Bondrov <abondrov@mandriva.org> 7.53-1mdv2011.0
+ Revision: 762908
- Fix file list (don't package same docs twice)
- New version 7.53

* Mon Oct 17 2011 Andrey Bondrov <abondrov@mandriva.org> 7.52-1
+ Revision: 704968
- New version 7.52

* Thu Apr 28 2011 Jani Välimaa <wally@mandriva.org> 7.51-2
+ Revision: 659805
- use _real_vendor macro in desktop file name

* Thu Apr 28 2011 Funda Wang <fwang@mandriva.org> 7.51-1
+ Revision: 659793
- fix group
- use vendor
- fix br with freetype2

  + Juan Luis Baptiste <juancho@mandriva.org>
    - Fixed group.
    - import alienarena

