Summary:	OCaml module manager
Summary(pl):	Zarz±dca modu³ów OCamla
Name:		ocaml-findlib
Version:	0.8.1
Release:	3
License:	distributable
Group:		Development/Tools
Vendor:		Gerd Stolpmann <gerd@gerd-stolpmann.de>
URL:		http://www.ocaml-programming.de/packages/
# Source0-md5:	b4643888d1a6626981113e23a92b9154
Source0:	http://www.ocaml-programming.de/packages/findlib-%{version}.tar.gz
BuildRequires:	ocaml >= 3.07
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
sed -i -e 's|/site-lib||' $RPM_BUILD_ROOT%{_libdir}/ocaml/topfind
ln -sf %{_libdir}/ocaml/topfind $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlfind
rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/findlib
cp -a $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/findlib
rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib/*.*
rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/findlib/META
echo 'directory = "+findlib"' >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/META
echo 'ldconf = "ignore"' >> $RPM_BUILD_ROOT%{_sysconfdir}/ocamlfind.conf

ln -s ../stublibs $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/libexec
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
%{_libdir}/ocaml/ocamlfind
%{_libdir}/ocaml/topfind
%{_mandir}/man3/*
