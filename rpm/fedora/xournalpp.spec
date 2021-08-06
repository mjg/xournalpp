%global         __cmake_in_source_build 0
%global         _gtest 1

#This spec file is intended for daily development snapshot release
%global	build_repo https://github.com/mjg/xournalpp/
%global	build_branch master
%global	version_string 1.1.0
%define	build_commit %(git ls-remote %{build_repo} | grep "refs/heads/%{build_branch}" | cut -c1-41)
%define	build_shortcommit %(c=%{build_commit}; echo ${c:0:7})
%global	build_timestamp %(date +"%Y%m%d")
%global	rel_build %{build_timestamp}git%{build_shortcommit}

Name:           xournalpp
Version:        %{version_string}^%{rel_build}
Release:        1%{?dist}
Summary:        Handwriting note-taking software

License:        GPLv2+
URL:            %{build_repo}
Source:         %{url}/archive/%{build_branch}.tar.gz

BuildRequires:  cmake >= 3.10
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  libappstream-glib
BuildRequires:  help2man
BuildRequires:  pkgconfig(glib-2.0) >= 2.32.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.18.9
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(portaudiocpp) >= 12
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  tex-latex-bin
Requires:       hicolor-icon-theme
Requires:       %{name}-plugins = %{version}-%{release}
Requires:       %{name}-ui = %{version}-%{release}
Requires:       texlive-scontents

%description
Xournal++ is a handwriting note-taking software with PDF annotation support.
Supports Pen input like Wacom Tablets

%package	plugins
Summary:        Default plugin for %{name}
BuildArch:      noarch

%description	plugins
The %{name}-plugins package contains sample plugins for  %{name}.

%package	ui
Summary:        User interface for %{name}
BuildArch:      noarch

%description	ui
The %{name}-ui package contains a graphical user interface for  %{name}.


%prep
%autosetup -n %{name}-%{build_branch}

%build
%cmake \
        %{?_gtest: -DENABLE_GTEST=ON} \
        -DENABLE_MATHTEX=ON \
        -DMAC_INTEGRATION=OFF 

%cmake_build

%install
%cmake_install

#Remove depreciated key from desktop file
#Fix desktop file associated with application
desktop-file-install \
 --remove-key="Encoding" \
 --set-key="StartupWMClass" \
 --set-value="xournalpp" \
  %{buildroot}%{_datadir}/applications/com.github.%{name}.%{name}.desktop
%find_lang %{name}

# REMOVE UNNECESSARY SCRIPTS
find %{buildroot}%{_datadir}/%{name} -name update-icon-cache.sh -delete -print

%fdupes %{buildroot}%{_datadir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.github.%{name}.%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.github.%{name}.%{name}.appdata.xml

%files -f %{name}.lang
%license LICENSE
%doc README.md AUTHORS
%{_bindir}/%{name}-thumbnailer
%{_bindir}/%{name}
%{_datadir}/applications/com.github.%{name}.%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/com.github.%{name}.%{name}.svg
%{_datadir}/icons/hicolor/scalable/mimetypes/*
%{_datadir}/mime/packages/com.github.%{name}.%{name}.xml
%exclude %{_datadir}/mimelnk/application/*
%{_datadir}/thumbnailers/com.github.%{name}.%{name}.thumbnailer
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/resources/*_template.tex
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/%{name}-thumbnailer.1.gz
%{_metainfodir}/com.github.%{name}.%{name}.appdata.xml

%files plugins
%{_datadir}/%{name}/plugins

%files ui
%{_datadir}/%{name}/ui

%changelog
* Sat Feb 20 2021 Luya Tshimbalanga <luya@fedoraproject.org>
- Add librsvg2 dependencies
- Add notice about daily git snapshot

* Mon Dec 16 2019 Luya Tshimbalanga <luya@fedoraproject.org>
- Implement some version autodetection to reduce maintenance work.
