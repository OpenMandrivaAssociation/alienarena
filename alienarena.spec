# source/unix/odesrc/ousrc/configure.ac explicitly references a number of files that don't exist
%define _disable_rebuild_configure 1
# -D_FORTIFY_SOURCE does #define dprintf -- but dprintf is used as a struct member here
%global _fortify_cflags %{nil}

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
Patch0:		alienarena-7.71.4-compile.patch
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
%autosetup -p1

# Copy license clarification for acebot
cp -p %{SOURCE2} .

# clean up end-line encoding
[[ -e docs/README.txt ]] && %{__sed} -i 's/\r//' docs/README.txt

# So, AlienArena now "uses" openal by dlopening the library, which is hardcoded to 
# "libopenal.so". That file only lives in openal-devel, so we need to adjust the hardcoding.
LIBOPENAL=`ls %{_libdir}/libopenal.so.? | cut -d "/" -f 4`
%__sed -i "s|\"libopenal.so\"|\"$LIBOPENAL\"|g" source/unix/qal_unix.c

export PTHREAD_CFLAGS="-pthread"
%configure

%build
%make_build

%install
%make_install

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor "%{_vendor}"		\
	--dir %{buildroot}%{_datadir}/applications	\
	%{SOURCE1}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
mv unix_dist/alien-arena.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

# opengl checker
ln -s opengl-game-wrapper.sh %{buildroot}%{_bindir}/%{name}-wrapper

# clean docs as we don't want to package them twice
rm -rf %{buildroot}%{_defaultdocdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc GPL.acebot.txt
%{_bindir}/%{name}
%{_bindir}/%{name}-wrapper
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/%{name}
%{_datadir}/icons/alienarena

%files server
%defattr(-,root,root,-)
%{_bindir}/alienarena-ded
