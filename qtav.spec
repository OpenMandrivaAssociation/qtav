%define major 1
%define libname %mklibname QtAV %{major}
%define devname %mklibname QtAV -d
%define wlibname %mklibname QtAVWidgets %{major}
%define wdevname %mklibname QtAVWidgets -d

%define oname QtAV

Name: qtav
Version: 1.13.0
Release: 1
Source0: https://github.com/wang-bin/QtAV/archive/v%{version}/%{oname}-%{version}.tar.gz
Source1: https://github.com/wang-bin/capi/archive/6a5f3006533b79aa57a3a54cf9df4442a356dd48.tar.gz
Source2: https://github.com/BYVoid/uchardet/archive/016eb18437793fbdd31149e1fe9fd73df3430d0f.tar.gz
Patch0: QtAV-1.12.0-linkage.patch
Patch1: qtav-1.12.0-fs-prefixes.patch
Summary: Multimedia playback framework based on Qt and FFmpeg
URL: http://qtav.org/
License: LGPL
Group: System/Libraries
BuildRequires: qmake5
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5OpenGL)
BuildRequires: cmake(Qt5Qml)
BuildRequires: cmake(Qt5Quick)
BuildRequires: cmake(Qt5Sql)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavdevice)
BuildRequires: pkgconfig(libavresample)
BuildRequires: pkgconfig(libswresample)
BuildRequires: pkgconfig(libva) >= 1.0.0 
BuildRequires: cmake
BuildRequires: ninja

%description
Multimedia playback framework based on Qt and FFmpeg

%package -n %{libname}
Summary: Multimedia playback framework based on Qt and FFmpeg
Group: System/Libraries

%description -n %{libname}
Multimedia playback framework based on Qt and FFmpeg

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name},
a multimedia playback framework based on Qt and FFmpeg

%package -n %{wlibname}
Summary: Multimedia playback framework based on QtWidgets and FFmpeg
Group: System/Libraries

%description -n %{wlibname}
Multimedia playback framework based on QtWidgets and FFmpeg

%package -n %{wdevname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{wlibname} = %{EVRD}

%description -n %{wdevname}
Development files (Headers etc.) for %{name},
a multimedia playback framework based on QtWidgets and FFmpeg

%prep
%setup -q -n %{oname}-%{version} -a 1 -a 2
%apply_patches
rmdir contrib/capi contrib/uchardet
mv capi-* contrib/capi
mv uchardet-* contrib/uchardet
%cmake_qt5 \
	-DQTAV_INSTALL_BINS=%{_bindir} \
	-DQTAV_INSTALL_LIBS=%{_libdir} \
	-DQTAV_INSTALL_QML=%{_libdir}/qt5/qml \
	-G Ninja

%build
%ninja -C build

%install
%ninja_install -C build

mkdir -p %{buildroot}%{_datadir}/applications
cat >%{buildroot}%{_datadir}/applications/%{name}.QMLPlayer.desktop <<'EOF'
[Desktop Entry]
Categories=Qt;AudioVideo;Player;Video;
Exec=QMLPlayer %U
GenericName=Media Player
Comment=Media player
MimeType=audio/ac3;audio/mp4;audio/mpeg;audio/vnd.rn-realaudio;audio/vorbis;audio/x-adpcm;audio/x-matroska;audio/x-mp2;audio/x-mp3;audio/x-ms-wma;audio/x-vorbis;audio/x-wav;audio/mpegurl;audio/x-mpegurl;audio/x-pn-realaudio;audio/x-scpls;audio/aac;audio/flac;audio/ogg;video/avi;video/mp4;video/flv;video/mpeg;video/quicktime;video/vnd.rn-realvideo;video/x-matroska;video/x-ms-asf;video/x-msvideo;video/x-ms-wmv;video/x-ogm;video/x-theora;video/webm;
Name=QMLPlayer
Type=Application
X-KDE-StartupNotify=true
EOF
sed -e 's,QMLPlayer,Player,g' %{buildroot}%{_datadir}/applications/%{name}.QMLPlayer.desktop >%{buildroot}%{_datadir}/applications/%{name}.Player.desktop
chmod +x %{buildroot}%{_datadir}/applications/*.desktop

%files
%{_bindir}/*
%{_datadir}/applications/*

%files -n %{libname}
%{_libdir}/libQtAV.so.%{major}*
%{_libdir}/qt5/qml/QtAV

%files -n %{devname}
%{_includedir}/QtAV
%{_libdir}/libQtAV.so
%{_libdir}/cmake/FindQtAV.cmake
%{_libdir}/cmake/QmlAV
%{_libdir}/cmake/QtAV

%files -n %{wlibname}
%{_libdir}/libQtAVWidgets.so.%{major}*

%files -n %{wdevname}
%{_includedir}/QtAVWidgets
%{_libdir}/libQtAVWidgets.so
%{_libdir}/cmake/QtAVWidgets
