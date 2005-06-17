#
# WARNING: despite unchanged SONAME, the RSA ABI (and API) has changed since 3.x!
#
# Conditional build:
%bcond_without	java	# build with Java support
%bcond_with	javac		# use javac instead of gcj
%bcond_without	python		# don't build python module
%bcond_without	doc		# don't build documentation
#
Summary:	The BeeCrypt Cryptography Library
Summary(pl):	Biblioteka kryptograficzna BeeCrypt
Name:		beecrypt
Version:	4.1.2
Release:	3
Epoch:		2
License:	LGPL
Group:		Libraries
Source0:	http://heanet.dl.sourceforge.net/beecrypt/%{name}-%{version}.tar.gz
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
BuildRequires:	gcc-java
%endif
%if %{with doc}
BuildRequires:	ghostscript
BuildRequires:	graphviz
%endif
%if %{with java} && %{with javac}
BuildRequires:	jdk
%endif
BuildRequires:	libtool
%if %{with java} && !%{with javac}
BuildRequires:	libgcj-devel
%endif
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-modules
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

%description -l pl
BeeCrypt jest open sourcow� bibliotek�, kt�ra zawiera wysoko
zoptymailzowane funkcje w C oraz assemblerze wielu algorytm�w
szyfrowania m.in.: Blowfish, MD5, SHA-1, Diffie-Hellman oraz ElGamal.

%package devel
Summary:	The BeeCrypt Cryptography Library - development files
Summary(pl):	Pliki dla programist�w u�ywaj�cych biblioteki BeeCrypt
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
The BeeCrypt Cryptography Library - development files.

%description devel -l pl
Biblioteka kryptograficzna BeeCrypt - pliki dla programist�w.

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

%package java
Summary:	BeeCrypt Java glue library
Summary(pl):	Biblioteka ��cz�ca BeeCrypt z Jav�
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description java
BeeCrypt Java glue library.

%description java -l pl
Biblioteka ��cz�ca BeeCrypt z Jav�.

%package java-devel
Summary:	Development files for BeeCrypt Java glue library
Summary(pl):	Pliki programistyczne biblioteki ��cz�cej Beecrypt z Jav�
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-java = %{epoch}:%{version}-%{release}

%description java-devel
Development files for BeeCrypt Java glue library.

%description java-devel -l pl
Pliki programistyczne biblioteki ��cz�cej Beecrypt z Jav�.

%package java-static
Summary:	BeeCrypt Java glue static library
Summary(pl):	Statyczna biblioteka ��cz�ca BeeCrypt z Jav�
Group:		Development/Libraries
Requires:	%{name}-java-devel = %{epoch}:%{version}-%{release}

%description java-static
BeeCrypt Java glue static library.

%description java-static -l pl
Statyczna biblioteka ��cz�ca BeeCrypt z Jav�.

%package -n python-beecrypt
Summary:	Python interface to BeeCrypt library
Summary(pl):	Pythonowy interfejs do biblioteki BeeCrypt
Group:		Development/Languages/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-beecrypt
The python-beecrypt package contains a module which permits applications
written in the Python programming language to use the interface
supplied by BeeCrypt libraries.

%description -n python-beecrypt -l pl
Pakiet python-beecrypt zawiera modu�, kt�ry pozwala aplikacjom napisanym w
Pythonie na u�ywanie interfejsu dostarczanego przez bibliotek� BeeCrytp.

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
	--with%{!?with_java:out}-javaglue \
	--with-cpu=%{_target_cpu} \
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

%post	java -p /sbin/ldconfig
%postun	java -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BENCHMARKS BUGS CONTRIBUTORS NEWS README
%attr(755,root,root) %{_libdir}/libbeecrypt.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbeecrypt.so
%{_libdir}/libbeecrypt.la
%{_includedir}/beecrypt

%files static
%defattr(644,root,root,755)
%{_libdir}/libbeecrypt.a

%if %{with java}
%files java
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbeecrypt_java.so.*.*.*

%files java-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbeecrypt_java.so
%{_libdir}/libbeecrypt_java.la

%files java-static
%defattr(644,root,root,755)
%{_libdir}/libbeecrypt_java.a
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/html/*
%endif 

%if %{with python}
%files -n python-beecrypt
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%endif
