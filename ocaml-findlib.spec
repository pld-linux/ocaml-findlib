Summary:	OCaml module manager
Summary(pl):	Zarz±dca modu³ów OCamla
Name:		ocaml-findlib
Version:	0.7.2
Release:	1
License:	distributable
Group:		Development/Tools
Vendor:		Gerd Stolpmann <gerd@gerd-stolpmann.de>
URL:		http://www.ocaml-programming.de/programming/page-4.html
Source0:	http://www.ocaml-programming.de/packages/findlib-%{version}.tar.gz
BuildRequires:	ocaml
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-labltk-devel
BuildRequires:	m4
%requires_eq	ocaml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The "findlib" library provides a scheme to manage reusable software
components (packages), and includes tools that support this scheme.
Packages are collections of OCaml modules for which metainformation
can be stored.

%description -l pl
Biblioteka "findlib" udostêpnia metodê zarz±dzania komponentami
oprogramowania (pakietami) oraz zawiera narzêdzia które ow± metodê
wspieraj±. Pakiety s± kolekcjami modu³ów w OCamlu, dla których jest
przechowywana metainformacja.

%package devel
Summary:	OCaml module manager
Summary(pl):	Zarz±dca modu³ów OCamla
Group:		Development/Libraries

%description devel
The "findlib" library provides a scheme to manage reusable software
components (packages), and includes tools that support this scheme.
Packages are collections of OCaml modules for which metainformation
can be stored.

This package includes libraries and compiled interfaces of findlib.

%description devel -l pl
Biblioteka "findlib" udostêpnia metodê zarz±dzania komponentami
oprogramowania (pakietami) oraz zawiera narzêdzia które ow± metodê
wspieraj±. Pakiety s± kolekcjami modu³ów w OCamlu, dla których jest
przechowywana metainformacja.

Ten pakiet zawiera biblioteki i skompilowane interfejsy findliba.

%prep
%setup -q -n findlib-%{version}

%build
./configure \
	-bindir %{_bindir} \
	-mandir %{_mandir} \
	-config %{_sysconfdir}/ocamlfind.conf

sed -e 's/-g//' Makefile > Makefile.tmp
mv -f Makefile.tmp Makefile

%{__make} all opt

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install PREFIX=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib/*.mli

# in PLD only META files are stored in site-lib/pkg
(sed -e 's|/site-lib||; s|use "findlib"|use "findlib.ml"|' \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/findlib
 echo 'directory = "+findlib"'
 ) > $RPM_BUILD_ROOT%{_libdir}/ocaml/findlib.ml
rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/findlib
cp -a $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/findlib
rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib/*.*

ln -s ../stublibs $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/stublibs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LICENSE doc/html
%attr(755,root,root) %{_bindir}/*
%config %{_sysconfdir}/ocamlfind.conf
%{_libdir}/ocaml/site-lib
%{_mandir}/man[15]/*

%files devel
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/findlib
%{_libdir}/ocaml/findlib/*.cm[ixa]*
%{_libdir}/ocaml/findlib/*.a
%{_mandir}/man3/*
