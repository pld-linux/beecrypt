#
# WARNING: despite unchanged SONAME, the RSA ABI (and API) has changed since 3.x!
# Conditional build:
%bcond_with	javaglue	# build with Java support
%bcond_without	python		# don't build python module
#
Summary:	The BeeCrypt Cryptography Library
Summary(pl):	Biblioteka kryptograficzna BeeCrypt
Name:		beecrypt
Version:	4.1.0
Release:	1
Epoch:		2
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/beecrypt/%{name}-%{version}.tar.gz
# Source0-md5:	073e224bdb27de411c2450717e9aa94c
Patch0:		%{name}-opt.patch
Patch1:		%{name}-lib64_fix.patch
Patch2:		%{name}-ac_python.patch
URL:		http://sourceforge.net/projects/beecrypt/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	libtool
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-modules
%endif
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex-dstroke
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_alpha		 -mno-explicit-relocs 

%description
BeeCrypt is an open source cryptography library that contains highly
optimized C and assembler implementations of many well-known
algorithms including Blowfish, MD5, SHA-1, Diffie-Hellman, and
ElGamal.

%description -l pl
BeeCrypt jest open sourcow± bibliotek±, która zawiera wysoko
zoptymailzowane funkcje w C oraz assemblerze wielu algorytmów
szyfrowania m.in.: Blowfish, MD5, SHA-1, Diffie-Hellman oraz ElGamal.

%package devel
Summary:	The BeeCrypt Cryptography Library - development files
Summary(pl):	Pliki dla programistów u¿ywaj±cych biblioteki BeeCrypt
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
The BeeCrypt Cryptography Library - development files.

%description devel -l pl
Biblioteka kryptograficzna BeeCrypt - pliki dla programistów.

%package static
Summary:	The BeeCrypt Cryptography Library - static library
Summary(pl):	Biblioteka statyczna BeeCrypt
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
The BeeCrypt Cryptography Library - static library.

%description static -l pl
Biblioteka statyczna BeeCrypt.

%package doc
Summary:	Development documentation for BeeCrypt
Summary(pl):	Dokumentacja programisty dla biblioteki BeeCrypt
Group:		Documentation

%description doc
Development documentation for BeeCrypt.

%description doc -l pl
Dokumentacja programisty dla biblioteki BeeCrypt.

%package -n python-beecrypt
Summary:	Python interface to BeeCrypt library
Summary(pl):	Pythonowy interfejs do biblioteki BeeCrypt
Group:		Development/Languages/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
%pyrequires_eq	python

%description -n python-beecrypt
The python-beecrypt package contains a module which permits applications
written in the Python programming language to use the interface
supplied by BeeCrypt libraries.

%description -n python-beecrypt -l pl
Pakiet python-beecrypt zawiera modu³, który pozwala aplikacjom napisanym w
Pythonie na u¿ywanie interfejsu dostarczanego przez bibliotekê BeeCrytp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# --with-cplusplus or building (even empty) *.cxx into libbeecrypt
# makes it (and thus rpm) depending on libstdc++ which is unacceptable
%{__perl} -pi -e 's/ cppglue\.cxx$//' Makefile.am
# only html docs
%{__perl} -pi -e 's/^GENERATE_LATEX .*/GENERATE_LATEX = NO/' Doxyfile.in

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--without-cplusplus \
	--with%{!?with_javaglue:out}-javaglue \
	--with-cpu=%{_target_cpu} \
	--with-arch=%{_target_cpu} \
	--with-pic \
	--with%{!?with_python:out}-python
%{__make}

%if %{with python}
%{__make} -C python
%endif

doxygen

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
%{__make} install -C python \
	DESTDIR=$RPM_BUILD_ROOT
%endif

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BENCHMARKS BUGS CONTRIBUTORS NEWS README
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files doc
%defattr(644,root,root,755)
%doc docs/html/*

%if %{with python}
%files -n python-beecrypt
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%endif
