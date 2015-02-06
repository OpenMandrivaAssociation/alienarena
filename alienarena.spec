#Based on Fedora's package
Name:		alienarena
Summary:	Multiplayer retro sci-fi deathmatch game
Version:	7.53
Release:	2
License:	GPLv2+
Group:		Games/Arcade
# Subversion:  https://svn.icculus.org/alienarena/trunk/?sortby=date
# Upstream seems too inept to provide a simple source only tarball, so we use svn.
#   svn export svn://svn.icculus.org/alienarena/tags/7.51/ alienarena-7.51/
# These windows files are useless to us.
#   rm -rf alienarena-7.51/*.exe alienarena-7.51/*.dll alienarena-7.51/Tools/aaradiant.exe 
# These bundled zips are also pretty useless.
#   rm -rf alienarena-7.51/lib_zipfiles/
# We don't want the bundled ode code.
#   rm -rf alienarena-7.51/source/unix/ode/
# arena/ botinfo/ data1/ live in the alienarena-data package
#   mkdir alienarena-data-20101216
#   mv alienarena-7.51/arena/ alienarena-7.51/botinfo/ alienarena-7.51/data1/ alienarena-data-20110323/
#   rm -f alienarena-data-20110323/{arena,data1}/game.so
# This data tarball is used for the alienarena-data package
#   tar -cvJf alienarena-data-20110323.tar.xz alienarena-data-20110323
# This source tarball is used for the alienarena package
#   tar -cvjf alienarena-7.51.tar.bz2 alienarena-7.51
Source0:	alienarena-%{version}.tar.xz
Source1:	alienarena.desktop
Source2:	GPL.acebot.txt
Patch3:		alienarena-7.45-no-qglBlitFramebufferEXT.patch
Patch4:		alienarena-7.51-nodata.patch
URL:		http://red.planetarena.org/
#BuildRequires:	libX11-devel 
BuildRequires:	libxext-devel
BuildRequires:	libxxf86vm-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmesagl-devel
BuildRequires:	libmesaglu-devel
BuildRequires:	curl-devel
BuildRequires:	libpng-devel
BuildRequires:	libvorbis-devel
BuildRequires:	openal-soft-devel
BuildRequires:	ode-devel
BuildRequires:	freetype2-devel
BuildRequires:	desktop-file-utils
Requires:	alienarena-data = 20120106
Requires:	desktop-file-utils >= 0.9
Requires:	opengl-games-utils
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
%setup -q

%patch3 -p1 -b .no-qglBlitFramebufferEXT
%patch4 -p1 -b .nodata

# Copy license clarification for acebot
%__cp -p %{SOURCE2} .

# clean up prebuilt binary files
[[ -e crx ]] && %__rm crded crx crx.sdl {arena,data1}/game.so

# clean up end-line encoding
[[ -e docs/README.txt ]] && %__sed -i 's/\r//' docs/README.txt

# So, AlienArena now "uses" openal by dlopening the library, which is hardcoded to 
# "libopenal.so". That file only lives in openal-devel, so we need to adjust the hardcoding.
LIBOPENAL=`ls %{_libdir}/libopenal.so.? | cut -d "/" -f 4`
%__sed -i "s|\"libopenal.so\"|\"$LIBOPENAL\"|g" source/unix/qal_unix.c

%build
export PTHREAD_LIBS="-lpthread"
export PTHREAD_CFLAGS="-pthread" 
%configure2_5x --with-system-libode --without-xf86dga
%make


%install
%__rm -rf %{buildroot}
%makeinstall_std

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

