#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	High-performance implementation of several "scalability protocols"
Summary(pl.UTF-8):	Wydajna implementacja kilku "protokołów skalowalności"
Name:		nanomsg
Version:	0.5
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: http://nanomsg.org/download.html
Source0:	http://download.nanomsg.org/%{name}-%{version}-beta.tar.gz
# Source0-md5:	65a79eabfc33e7a55e2293e12c367f73
URL:		http://nanomsg.org/
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1.6
BuildRequires:	libtool >= 2:2
BuildRequires:	xmlto
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
%setup -q -n %{name}-%{version}-beta

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-doc \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnanomsg.la
# HTML version of man pages (generated from the same asciidoc sources)
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/nanomsg

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%attr(755,root,root) %{_bindir}/nanocat
%attr(755,root,root) %{_bindir}/nn_*
%attr(755,root,root) %{_libdir}/libnanomsg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnanomsg.so.0
%{_mandir}/man1/nanocat.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnanomsg.so
%{_includedir}/nanomsg
%{_pkgconfigdir}/libnanomsg.pc
%{_mandir}/man3/nn_*.3*
%{_mandir}/man7/nanomsg.7*
%{_mandir}/man7/nn_*.7*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnanomsg.a
%endif
