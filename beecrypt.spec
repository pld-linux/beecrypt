Summary:	The BeeCrypt Cryptography Library
Name:		beecrypt
Version:	2.1.0
Release:	1
License:	LGPL
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Source0:	http://www.virtualunlimited.com/download/%{name}-%{version}.tar.gz
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	libtool
URL:		http://beecrypt.virtualunlimited.com/
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BeeCrypt is an open source cryptography library that contains highly
optimized C and assembler implementations of many well-known
algorithms including Blowfish, MD5, SHA-1, Diffie-Hellman, and
ElGamal.

%description -l pl
BeeCrypt jest open sourcow╠ bibliotek╠, ktСra zawiera wysoko
zoptymailzowane funkcje w C oraz assemblerze wielu algorytmСw
szyfrowania m.in. : Blowfish, MD5, SHA-1, Diffie-Hellman oraz ElGamal.

%package devel
Summary:	The BeeCrypt Cryptography Library - development files
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name} = %{version}

%description devel
The BeeCrypt Cryptography Library - development files.

%package static
Summary:	The BeeCrypt Cryptography Library - static library
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name}-devel = %{version}

%description static
The BeeCrypt Cryptography Library - static library.

%prep
%setup -q

%build
#rm -f missing
#libtoolize --copy --force
#aclocal
#autoconf
#automake -a -c
%configure2_13 \
	--enable-static \
	--%{?debug:en}%{!?debug:dis}able-debug
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf AUTHORS BENCHMARKS BUGS CONTRIBUTORS ChangeLog NEWS README

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BUGS* NEWS* README*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc AUTHORS* BENCHMARKS* CONTRIBUTORS* ChangeLog*
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/beecrypt

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
