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
URL:		http://beecrypt.virtualunlimited.com/
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%package devel
Requires:	beecrypt = %{version}
Summary:	The BeeCrypt Cryptography Library headers
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки

%description
BeeCrypt is an open source cryptography library that contains highly
optimized C and assembler implementations of many well-known
algorithms including Blowfish, MD5, SHA-1, Diffie-Hellman, and
ElGamal.

%description -l pl
BeeCrypt jest open sourcow╠ bibliotek╠, ktСra zawiera wysoko
zoptymailzowane funkcje w C oraz assemblerze wielu algorytmСw
szyfrowania m.in. : Blowfish, MD5, SHA-1, Diffie-Hellman oraz ElGamal.

%description devel
Biblioteki do pakietu BeeCrypt.

%description devel -l pl
Biblioteki do pakietu BeeCrypt.

%prep
%setup -q

%build
./configure --prefix=%{buildroot}%{_prefix} --target=%{_target}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install

%clean
make clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%{_libdir}/libbeecrypt.la
%{_libdir}/libbeecrypt.so.2.1.0

%post
ln -s /usr/lib/libbeecrypt.so.2.1.0 /usr/lib/libbeecrypt.so
ln -s /usr/lib/libbeecrypt.so.2.1.0 /usr/lib/libbeecrypt.so.2

%postun
rm -f /usr/lib/libbeecrypt.so.2.1.0
rm -f /usr/lib/libbeecrypt.so.2
rm -f /usr/lib/libbeecrypt.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/beecrypt/base64.h
%{_includedir}/beecrypt/beecrypt.h
%{_includedir}/beecrypt/blockmode.h
%{_includedir}/beecrypt/blockpad.h
%{_includedir}/beecrypt/blowfish.h
%{_includedir}/beecrypt/blowfishopt.h
%{_includedir}/beecrypt/dhaes.h
%{_includedir}/beecrypt/dldp.h
%{_includedir}/beecrypt/dlkp.h
%{_includedir}/beecrypt/dlpk.h
%{_includedir}/beecrypt/dlsvdp-dh.h
%{_includedir}/beecrypt/elgamal.h
%{_includedir}/beecrypt/endianness.h
%{_includedir}/beecrypt/entropy.h
%{_includedir}/beecrypt/fips180.h
%{_includedir}/beecrypt/fips180opt.h
%{_includedir}/beecrypt/fips186.h
%{_includedir}/beecrypt/hmac.h
%{_includedir}/beecrypt/hmacmd5.h
%{_includedir}/beecrypt/hmacsha1.h
%{_includedir}/beecrypt/hmacsha256.h
%{_includedir}/beecrypt/md5.h
%{_includedir}/beecrypt/memchunk.h
%{_includedir}/beecrypt/mp32.h
%{_includedir}/beecrypt/mp32opt.h
%{_includedir}/beecrypt/mp32barrett.h
%{_includedir}/beecrypt/mp32number.h
%{_includedir}/beecrypt/mp32prime.h
%{_includedir}/beecrypt/mtprng.h
%{_includedir}/beecrypt/rsa.h
%{_includedir}/beecrypt/rsakp.h
%{_includedir}/beecrypt/rsapk.h
%{_includedir}/beecrypt/sha256.h
%{_includedir}/beecrypt/timestamp.h
