#
# WARNING: despite unchanged SONAME, the RSA ABI (and API) has changed since 3.x!
#
# Conditional build:
%bcond_without	java	# build with Java support
%bcond_with	javac		# use javac instead of gcj
%bcond_without	python		# don't build python module
%bcond_without	doc		# don't build documentation
%bcond_without	static_libs	# don't build static libraries
#
Summary:	The BeeCrypt Cryptography Library
Summary(pl.UTF-8):	Biblioteka kryptograficzna BeeCrypt
Name:		beecrypt
Version:	4.1.2
Release:	8
Epoch:		2
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/beecrypt/%{name}-%{version}.tar.gz
# Source0-md5:	820d26437843ab0a6a8a5151a73a657c
Patch0:		%{name}-opt.patch
Patch1:		%{name}-lib64_fix.patch
Patch2:		%{name}-ac_python.patch
URL:		http://sourceforge.net/projects/beecrypt/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%if %{with doc}
BuildRequires:	doxygen
%endif
%if %{with java} && !%{with javac}
%ifarch i586 i686 athlon pentium3 pentium4 %{x8664}
BuildRequires:	jdk
%else
BuildRequires:	gcc-java
BuildRequires:	libgcj-devel
%endif
%endif
%if %{with doc}
BuildRequires:	ghostscript
BuildRequires:	graphviz
%endif
%if %{with java} && %{with javac}
BuildRequires:	jdk
%endif
BuildRequires:	libtool
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
%endif
BuildRequires:	rpmbuild(macros) >= 1.213
%if %{with doc}
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex-dstroke
# note: this is incorrect place, it should be somewhere in tetex packages
BuildRequires:	tetex-metafont
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_alpha		 -mno-explicit-relocs

%description
BeeCrypt is an open source cryptography library that contains highly
optimized C and assembler implementations of many well-known
algorithms including Blowfish, MD5, SHA-1, Diffie-Hellman, and
ElGamal.

%description -l pl.UTF-8
BeeCrypt jest open sourcową biblioteką, która zawiera wysoko
zoptymailzowane funkcje w C oraz assemblerze wielu algorytmów
szyfrowania m.in.: Blowfish, MD5, SHA-1, Diffie-Hellman oraz ElGamal.

%package devel
Summary:	The BeeCrypt Cryptography Library - development files
Summary(pl.UTF-8):	Pliki dla programistów używających biblioteki BeeCrypt
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
The BeeCrypt Cryptography Library - development files.

%description devel -l pl.UTF-8
Biblioteka kryptograficzna BeeCrypt - pliki dla programistów.

%package static
Summary:	The BeeCrypt Cryptography Library - static library
Summary(pl.UTF-8):	Biblioteka statyczna BeeCrypt
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
The BeeCrypt Cryptography Library - static library.

%description static -l pl.UTF-8
Biblioteka statyczna BeeCrypt.

%package doc
Summary:	Development documentation for BeeCrypt
Summary(pl.UTF-8):	Dokumentacja programisty dla biblioteki BeeCrypt
Group:		Documentation

%description doc
Development documentation for BeeCrypt.

%description doc -l pl.UTF-8
Dokumentacja programisty dla biblioteki BeeCrypt.

%package java
Summary:	BeeCrypt Java glue library
Summary(pl.UTF-8):	Biblioteka łącząca BeeCrypt z Javą
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description java
BeeCrypt Java glue library.

%description java -l pl.UTF-8
Biblioteka łącząca BeeCrypt z Javą.

%package java-devel
Summary:	Development files for BeeCrypt Java glue library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki łączącej Beecrypt z Javą
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-java = %{epoch}:%{version}-%{release}

%description java-devel
Development files for BeeCrypt Java glue library.

%description java-devel -l pl.UTF-8
Pliki programistyczne biblioteki łączącej Beecrypt z Javą.

%package java-static
Summary:	BeeCrypt Java glue static library
Summary(pl.UTF-8):	Statyczna biblioteka łącząca BeeCrypt z Javą
Group:		Development/Libraries
Requires:	%{name}-java-devel = %{epoch}:%{version}-%{release}

%description java-static
BeeCrypt Java glue static library.

%description java-static -l pl.UTF-8
Statyczna biblioteka łącząca BeeCrypt z Javą.

%package -n python-beecrypt
Summary:	Python interface to BeeCrypt library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki BeeCrypt
Group:		Development/Languages/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-beecrypt
The python-beecrypt package contains a module which permits
applications written in the Python programming language to use the
interface supplied by BeeCrypt libraries.

%description -n python-beecrypt -l pl.UTF-8
Pakiet python-beecrypt zawiera moduł, który pozwala aplikacjom
napisanym w Pythonie na używanie interfejsu dostarczanego przez
bibliotekę BeeCrytp.

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
	%{?with_javac:ac_cv_have_gcj=no} \
	--without-cplusplus \
	--with%{!?with_java:out}-java \
	--with-cpu=%{_target_cpu} \
	%{!?with_static_libs:--enable-static=no} \
%ifarch %{x8664}
	--with-arch=x86_64 \
%else
	--with-arch=%{_target_cpu} \
%endif
	--with-pic \
	--with%{!?with_python:out}-python
%{__make}

%if %{with python}
%{__make} -C python
%endif

%if %{with doc}
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
%{__make} install -C python \
	DESTDIR=$RPM_BUILD_ROOT
%endif

mv -f $RPM_BUILD_ROOT%{_libdir}/libbeecrypt.so.*.*.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libbeecrypt.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libbeecrypt.so

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	java -p /sbin/ldconfig
%postun	java -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BENCHMARKS BUGS CONTRIBUTORS NEWS README
%attr(755,root,root) /%{_lib}/libbeecrypt.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbeecrypt.so
%{_libdir}/libbeecrypt.la
%{_includedir}/beecrypt

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbeecrypt.a
%endif

%if %{with java}
%files java
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbeecrypt_java.so.*.*.*

%files java-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbeecrypt_java.so
%{_libdir}/libbeecrypt_java.la

%if %{with static_libs}
%files java-static
%defattr(644,root,root,755)
%{_libdir}/libbeecrypt_java.a
%endif
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/html
%endif

%if %{with python}
%files -n python-beecrypt
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%endif
