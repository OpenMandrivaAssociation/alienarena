#Based on Fedora's package
Name:		alienarena
Summary:	Multiplayer retro sci-fi deathmatch game
Version:	7.51
Release:	%mkrel 1
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
Source0:	alienarena-%{version}.tar.bz2
Source1:	alienarena.desktop
Source2:	GPL.acebot.txt
Patch3:		alienarena-7.45-no-qglBlitFramebufferEXT.patch
Patch4:		alienarena-7.51-nodata.patch
#Patch5:		alienarena-7.51-system-ode-double.patch
URL:		http://red.planetarena.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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
BuildRequires:	freetype-devel
BuildRequires:	desktop-file-utils
Requires:	alienarena-data = 20110323
Requires:	desktop-file-utils >= 0.9
Requires:	opengl-games-utils
Requires:	openal

%description
Alien Arena 2011 is an online deathmatch game with over 30 levels, seven modes 
of play, loads of mutators, built-in bots, multiple player characters and weapons
(with alt-fire modes).


%package server
Group:		Amusements/Games
Summary:	Dedicated server for alienarena, the FPS game
Requires:	alienarena-data = 20110323


%description server
Alien Arena 2011 is an online deathmatch game with over 30 levels, seven modes
of play, loads of mutators, built-in bots, multiple player characters and weapons
(with alt-fire modes).

This is the dedicated server.


%prep
%setup -q

%patch3 -p1 -b .no-qglBlitFramebufferEXT
%patch4 -p1 -b .nodata
#%patch5 -p1 -b .ode-double

# Copy license clarification for acebot
cp -p %{SOURCE2} .

# clean up prebuilt binary files
[[ -e crx ]] && rm crded crx crx.sdl {arena,data1}/game.so

# clean up end-line encoding
[[ -e docs/README.txt ]] && %{__sed} -i 's/\r//' docs/README.txt

# So, AlienArena now "uses" openal by dlopening the library, which is hardcoded to 
# "libopenal.so". That file only lives in openal-devel, so we need to adjust the hardcoding.
LIBOPENAL=`ls %{_libdir}/libopenal.so.? | cut -d "/" -f 4`
sed -i "s|\"libopenal.so\"|\"$LIBOPENAL\"|g" source/unix/qal_unix.c

%build
export PTHREAD_LIBS="-lpthread"
export PTHREAD_CFLAGS="-pthread" 
%configure --with-system-libode --without-xf86dga
%make


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%{__mkdir_p} %{buildroot}%{_datadir}/applications
desktop-file-install --vendor "mandriva"			\
	--dir %{buildroot}%{_datadir}/applications	\
	%{SOURCE1}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
mv %{buildroot}%{_datadir}/icons/%{name}.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

# opengl checker
ln -s opengl-game-wrapper.sh %{buildroot}/%{_bindir}/%{name}-wrapper
ln -s crx %{buildroot}/%{_bindir}/%{name}
ln -s crx-ded %{buildroot}/%{_bindir}/%{name}-server

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%files
%defattr(-,root,root,-)
%doc GPL.acebot.txt
%{_bindir}/crx
%{_bindir}/%{name}
%{_bindir}/%{name}-wrapper
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_defaultdocdir}/%{name}/

%files server
%defattr(-,root,root,-)
%{_bindir}/crx-ded
%{_bindir}/%{name}-server
%{_defaultdocdir}/%{name}/

