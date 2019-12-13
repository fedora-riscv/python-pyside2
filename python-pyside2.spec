%global pypi_name pyside2
%global camel_name PySide2

# Clang doesn't handle some gcc specific flags.
%global _optflags %optflags
%global optflags %(echo %optflags | sed 's| -fstack-clash-protection||')
%global optflags %(echo %optflags | sed 's| -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1||')
%global optflags %(echo %optflags | sed 's| -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1||')

Name:           python-%{pypi_name}
Epoch:          1
Version:        5.13.2
Release:        1%{?dist}
Summary:        Python bindings for the Qt 5 cross-platform application and UI framework

License:        BSD and GPLv2 and GPLv3 and LGPLv3
URL:            https://wiki.qt.io/Qt_for_Python

Source0:        https://download.qt.io/official_releases/QtForPython/%{pypi_name}/%{camel_name}-%{version}-src/pyside-setup-opensource-src-%{version}.tar.xz

# Don't abort the build on Python 3.8
Patch0:         python38_classifier.patch

BuildRequires:  cmake gcc graphviz
BuildRequires:  clang-devel llvm-devel
BuildRequires:  /usr/bin/pathfix.py
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
# Shiboken2
BuildRequires:  qt5-qtbase-devel > 5.13
BuildRequires:  qt5-qtxmlpatterns-devel  > 5.13
BuildRequires:  qt5-qtwebkit-devel
# Needed for Cmake UI Config
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtx11extras-devel
# PySide2
BuildRequires:  qt5-qtbase-private-devel >= 5.13
BuildRequires:  qt5-qtcharts-devel > 5.13
BuildRequires:  qt5-qtdatavis3d-devel > 5.13
BuildRequires:  qt5-qtremoteobjects-devel > 5.13
BuildRequires:  qt5-qtscript-devel > 5.13
BuildRequires:  qt5-qtmultimedia-devel > 5.13
BuildRequires:  qt5-qtxmlpatterns-devel > 5.13
BuildRequires:  qt5-qttools-devel > 5.13
BuildRequires:  qt5-qtmultimedia-devel > 5.13
BuildRequires:  qt5-qtscxml-devel > 5.13
BuildRequires:  qt5-qtsensors-devel > 5.13
BuildRequires:  qt5-qtspeech-devel > 5.13
BuildRequires:  qt5-qtsvg-devel > 5.13
%ifnarch ppc64le s390x
BuildRequires:  qt5-qtwebengine-devel > 5.13
%endif
BuildRequires:  qt5-qtwebsockets-devel > 5.13
BuildRequires:  qt5-qt3d-devel > 5.13
BuildRequires:  qt5-qttools-devel > 5.13


%description
PySide2 is the official Python module from the Qt for Python project, which
provides access to the complete Qt 5.13+ framework.

The name Shiboken2 and PySide2 make reference to the Qt 5 compatibility, since
the previous versions (without the 2) refer to Qt 4.

%package -n     python3-%{pypi_name}
Provides:       python3-%{camel_name} = %{version}-%{release}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
%{?python_provide:%python_provide python3-%{camel_name}}

%description -n python3-%{pypi_name}
PySide2 is the official Python module from the Qt for Python project, which
provides access to the complete Qt 5.13+ framework.

The name Shiboken2 and PySide2 make reference to the Qt 5 compatibility, since
the previous versions (without the 2) refer to Qt 4.


%package -n     python3-%{pypi_name}-devel
Requires:       pyside2-tools
Requires:       shiboken2
Summary:        Development files related to %{name}
%{?python_provide:%python_provide python3-%{pypi_name}-devel}
%{?python_provide:%python_provide python3-%{camel_name}-devel}

%description -n python3-%{pypi_name}-devel
%{summary}.


%package -n pyside2-tools
Summary:        PySide2 tools for the Qt 5 framework

%description -n pyside2-tools
PySide2 provides Python bindings for the Qt5 cross-platform application
and UI framework.

This package ships the following accompanying tools:
 * pyside2-rcc - PySide2 resource compiler
 * pyside2-uic - Python User Interface Compiler for PySide2
 * pyside2-lupdate - update Qt Linguist translation files for PySide2

The name Shiboken2 and PySide2 make reference to the Qt 5 compatibility, since
the previous versions (without the 2) refer to Qt 4.


%package -n shiboken2
Summary:        Python / C++ bindings generator for %camel_name

%description -n shiboken2
Shiboken is the Python binding generator that Qt for Python uses to create the
PySide module, in other words, is the system we use to expose the Qt C++ API to
Python.

The name Shiboken2 and PySide2 make reference to the Qt 5 compatibility, since
the previous versions (without the 2) refer to Qt 4.

%package -n python3-shiboken2
Summary:        Python / C++ bindings libraries for %camel_name

%description -n python3-shiboken2
Shiboken is the Python binding generator that Qt for Python uses to create the
PySide module, in other words, is the system we use to expose the Qt C++ API to
Python.

The name Shiboken2 and PySide2 make reference to the Qt 5 compatibility, since
the previous versions (without the 2) refer to Qt 4.

%package -n python3-shiboken2-devel
Summary:        Python / C++ bindings helper module for %camel_name
Requires:       shiboken2
Requires:       python3-shiboken2

%description -n python3-shiboken2-devel
Shiboken is the Python binding generator that Qt for Python uses to create the
PySide module, in other words, is the system we use to expose the Qt C++ API to
Python.

The name Shiboken2 and PySide2 make reference to the Qt 5 compatibility, since
the previous versions (without the 2) refer to Qt 4.


%prep
%autosetup -p1 -n pyside-setup-opensource-src-%{version}


%build
export CXX=/usr/bin/clang++
mkdir %{_target} && cd %{_target}
%cmake -DUSE_PYTHON_VERSION=3 ../
%make_build


%install
cd %{_target}
%make_install
cd -

# Remove v2 files that bytecompile chokes on...
rm -rf %{buildroot}%{python3_sitearch}/pyside2uic/port_v2

# Generate egg-info manually and install since we're performing a cmake build.
%{__python3} setup.py egg_info
for name in PySide2 shiboken2 shiboken2_generator; do
  mkdir -p %{buildroot}%{python3_sitearch}/$name-%{version}-py%{python3_version}.egg-info
  cp -p $name.egg-info/{PKG-INFO,not-zip-safe,top_level.txt} \
        %{buildroot}%{python3_sitearch}/$name-%{version}-py%{python3_version}.egg-info/
done

# Fix all Python shebangs recursively
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
# Need to list files that do not match ^[a-zA-Z0-9_]+\.py$ explicitly!
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_bindir}/*
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_bindir}/pyside2-uic

# icon_cache is not executable and therefore  should not have a shebang
sed -i '/^#!/d' %{buildroot}%{python3_sitearch}/pyside2uic/icon_cache.py


%check
# Lots of tests fail currently
# Also, the testing doesn't appear to work with the direct CMake build method.
#{__python3} testrunner.py test


%files -n python3-%{pypi_name}
%license LICENSE.LGPLv3
%doc README.md
%doc CHANGES.rst
%{_libdir}/libpyside2*.so.5.13*
%{python3_sitearch}/%{camel_name}/
%{python3_sitearch}/%{camel_name}-%{version}-py%{python3_version}.egg-info/

%files -n python3-%{pypi_name}-devel
%{_datadir}/PySide2/
%{_includedir}/PySide2/
%{_libdir}/libpyside2*.so
%{_libdir}/cmake/PySide2*
%{_libdir}/pkgconfig/pyside2.pc

%files -n pyside2-tools
%doc README.pyside*
%license LICENSE.GPL2
%{_bindir}/pyside*
%{_mandir}/man1/pyside*.1*
%{python3_sitearch}/pyside2uic/

%files -n shiboken2
%doc README.shiboken2-generator.md
%license LICENSE.GPLv3
%{_bindir}/shiboken2
%{_bindir}/shiboken_tool.py
%{_mandir}/man1/shiboken2.1.*

%files -n python3-shiboken2
%doc README.shiboken2.md
%license LICENSE.LGPLv3
%{_libdir}/libshiboken2*.so.5.13*
%{python3_sitearch}/shiboken2/
%{python3_sitearch}/shiboken2-%{version}-py%{python3_version}.egg-info/

%files -n python3-shiboken2-devel
%doc README.shiboken2.md
%{_includedir}/shiboken2/
%{_libdir}/cmake/Shiboken2-%{version}/
%{_libdir}/libshiboken2*.so
%{_libdir}/pkgconfig/shiboken2.pc
%{python3_sitearch}/shiboken2_generator/
%{python3_sitearch}/shiboken2_generator-%{version}-py%{python3_version}.egg-info/


%changelog
* Fri Dec 13 2019 Richard Shaw <hobbes1069@gmail.com> - 1:5.13.2-1
- Update to 5.13.2.

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 1:5.12.6-2
- rebuild (qt5)

* Fri Nov 22 2019 Richard Shaw <hobbes1069@gmail.com> - 1:5.12.6-1
- Update to 5.12.6.

* Wed Oct 09 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.12.5-1.1
- branch rebuild (qt5)

* Mon Sep 30 2019 Richard Shaw <hobbes1069@gmail.com> - 1:5.12.5-1
- Downgrade to 5.12.5 as the MAJOR & MINOR versions must match Qt.

* Wed Sep 25 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.1-2
- rebuild (qt5)

* Mon Sep 09 2019 Richard Shaw <hobbes1069@gmail.com> - 5.13.1-1
- Update to 5.13.1.

* Thu Aug 15 2019 Richard Shaw <hobbes1069@gmail.com> - 5.12.4-1
- Update to 5.12.4.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 09 2019 Richard Shaw <hobbes1069@gmail.com> - 5.12.3-1
- Update to 5.12.3.

* Tue Jun 04 2019 Richard Shaw <hobbes1069@gmail.com> - 5.12.1-4
- Change python3-shiboken-libs to python3-shiboken.

* Tue Apr 23 2019 Richard Shaw <hobbes1069@gmail.com> - 5.12.1-3
- Update per review comments.
- Make library globs dependent  on soname.
- Add explicit requires for skiboken2 on shiboken2-devel.
- Try to workaround qt5-qtwebengine not being available on ppc64le and s390x.

* Thu Apr 18 2019 Richard Shaw <hobbes1069@gmail.com> - 5.12.1-2
- Update spec per review request comments.

* Sat Mar 02 2019 Richard Shaw <hobbes1069@gmail.com> - 5.12.1-1
- Update to 5.12.1 now that the correct version of Qt5 is in Rawhide.

* Tue Feb 05 2019 Miro Hrončok <mhroncok@redhat.com> - 5.11.22-1
- Inital package
