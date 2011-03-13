%define		ocaml_ver	1:3.09.2
Summary:	OCaml module manager
Summary(pl.UTF-8):	Zarządca modułów OCamla
Name:		ocaml-findlib
Version:	1.2.6
Release:	1
License:	distributable
Group:		Development/Tools
Source0:	http://download.camlcity.org/download/findlib-%{version}.tar.gz
# Source0-md5:	4924c8c3ef1208eb0fa9096c8b8bb72f
URL:		http://www.ocaml-programming.de/packages/
BuildRequires:	m4
BuildRequires:	ncurses-devel
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-labltk-devel
BuildRequires:	sed >= 4.0
%requires_eq	ocaml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The "findlib" library provides a scheme to manage reusable software
components (packages), and includes tools that support this scheme.
Packages are collections of OCaml modules for which metainformation
can be stored.

%description -l pl.UTF-8
Biblioteka "findlib" udostępnia metodę zarządzania komponentami
oprogramowania (pakietami) oraz zawiera narzędzia, które ową metodę
wspierają. Pakiety są kolekcjami modułów w OCamlu, dla których mogą
być przechowywane metainformacje.

%package devel
Summary:	OCaml module manager
Summary(pl.UTF-8):	Zarządca modułów OCamla
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The "findlib" library provides a scheme to manage reusable software
components (packages), and includes tools that support this scheme.
Packages are collections of OCaml modules for which metainformation
can be stored.

This package includes libraries and compiled interfaces of findlib.

%description devel -l pl.UTF-8
Biblioteka "findlib" udostępnia metodę zarządzania komponentami
oprogramowania (pakietami) oraz zawiera narzędzia, które ową metodę
wspierają. Pakiety są kolekcjami modułów w OCamlu, dla których mogą
być przechowywane metainformacje.

Ten pakiet zawiera biblioteki i skompilowane interfejsy findliba.

%prep
%setup -q -n findlib-%{version}

%build
./configure \
	-bindir %{_bindir} \
	-mandir %{_mandir} \
	-config %{_sysconfdir}/ocamlfind.conf

sed -i -e 's/-g//' Makefile

%{__make} -j1 all opt

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib/*.mli

# in PLD only META files are stored in site-lib/pkg
sed -i -e 's|/site-lib||' $RPM_BUILD_ROOT%{_libdir}/ocaml/topfind
ln -sf %{_libdir}/ocaml/topfind $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlfind
cp -a $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/findlib
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib/*.*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/findlib/META
echo 'directory = "+findlib"' >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/META
echo 'ldconf = "ignore"' >> $RPM_BUILD_ROOT%{_sysconfdir}/ocamlfind.conf

ln -s ../stublibs $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/libexec
ln -s ../stublibs $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/stublibs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/README LICENSE doc/*-html
%attr(755,root,root) %{_bindir}/ocamlfind
%attr(755,root,root) %{_bindir}/safe_camlp4
%config %{_sysconfdir}/ocamlfind.conf
%{_libdir}/ocaml/site-lib
%{_mandir}/man1/ocamlfind.1*
%{_mandir}/man5/META.5*
%{_mandir}/man5/findlib.conf.5*
%{_mandir}/man5/site-lib.5*

%files devel
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/findlib
%{_libdir}/ocaml/findlib/*.cm[ixa]*
%{_libdir}/ocaml/findlib/*.a
%{_libdir}/ocaml/ocamlfind
%{_libdir}/ocaml/topfind
