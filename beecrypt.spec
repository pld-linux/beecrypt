#
# Conditional build:
# _with_javaglue
#
%include	/usr/lib/rpm/macros.python
Summary:	The BeeCrypt Cryptography Library
Summary(pl):	Biblioteka kryptograficzna BeeCrypt
Name:		beecrypt
Version:	3.0.0
Release:	1
Epoch:		2
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/beecrypt/%{name}-%{version}.tar.gz
# Source0-md5:	18f20c22443f85bd4e285925b56198d9
Patch0:		%{name}-opt.patch
Patch1:		%{name}-python.patch
URL:		http://sourceforge.net/projects/beecrypt/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	%{name} = %{version}

%description devel
The BeeCrypt Cryptography Library - development files.

%description devel -l pl
Biblioteka kryptograficzna BeeCrypt - pliki dla programistów.

%package static
Summary:	The BeeCrypt Cryptography Library - static library
Summary(pl):	Biblioteka statyczna BeeCrypt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
The BeeCrypt Cryptography Library - static library.

%description static -l pl
Biblioteka statyczna BeeCrypt.

%package -n python-beecrypt
Summary:	Python interface to BeeCrypt library
Summary(pl):	Pythonowy interfejs do biblioteki BeeCrypt
Group:		Development/Languages/Python
Requires:	%{name} = %{version}
%pyrequires_eq	python

%description -n python-beecrypt
The python-beecrypt package contains a module which permits applications
written in the Python programming language to use the interface
supplied by BeeCrypt libraries.

%description -n python-beecrypt -l pl
Pakiet python-beecrypt zawiera modu³, który pozwala aplikacjom napisanym w
Pythonie na u¿ywanie interfejsu dostarczanego przez bibliotekê BeeCrytp.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with%{?!_with_javaglue:out}-javaglue \
	--with-cpu=%{_target_cpu} \
	--with-arch=%{_target_cpu}
%{__make}

%{__make} -C python

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install -C python \
	DESTDIR=$RPM_BUILD_ROOT

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
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n python-beecrypt
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
