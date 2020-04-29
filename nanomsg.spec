#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	High-performance implementation of several "scalability protocols"
Summary(pl.UTF-8):	Wydajna implementacja kilku "protokołów skalowalności"
Name:		nanomsg
Version:	1.1.5
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/nanomsg/nanomsg/releases
Source0:	https://github.com/nanomsg/nanomsg/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	272db464bac1339b6cea060dd63b22d4
Patch0:		%{name}-nolibs.patch
URL:		https://nanomsg.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	ruby-asciidoctor
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nanomsg library is a simple high-performance implementation of several
"scalability protocols". Scalability protocol's job is to define how
multiple applications communicate to form a single distributed
application.

%description -l pl.UTF-8
Biblioteka nanomsg to prosta, wydajna implementacja kilku "protokołów
skalowalności". Zadaniem takiego protokołu jest określenie, jak wiele
aplikacji powinno się komunikować w celu stworzenia pojedynczej
aplikacji rozproszonej.

%package devel
Summary:	Header files for nanomsg library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki nanomsg
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for nanomsg library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki nanomsg.

%package static
Summary:	Static nanomsg library
Summary(pl.UTF-8):	Statyczna biblioteka nanomsg
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static nanomsg library.

%description static -l pl.UTF-8
Statyczna biblioteka nanomsg.

%prep
%setup -q
%patch0 -p1

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DNN_STATIC_LIB=ON \
	-DCMAKE_INSTALL_LIDBIR=%{_lib}

%{__make}
cd ..
%endif

install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_LIDBIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# HTML version of man pages (generated from the same asciidoc sources)
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/*.html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README.md SUPPORT
%attr(755,root,root) %{_bindir}/nanocat
%attr(755,root,root) %{_libdir}/libnanomsg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnanomsg.so.5
%{_mandir}/man1/nanocat.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnanomsg.so
%{_includedir}/nanomsg
%{_pkgconfigdir}/nanomsg.pc
%{_libdir}/cmake/nanomsg-%{version}
%{_mandir}/man3/nn_*.3*
%{_mandir}/man7/nanomsg.7*
%{_mandir}/man7/nn_*.7*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnanomsg.a
%endif
