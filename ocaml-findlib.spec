Summary:	OCaml module manager
Summary(pl):	Zarz±dca modu³ów OCamla
Name:		ocaml-findlib
Version:	0.6.2
Release:	1
License:	distributable
Group:		Development/Libraries
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

%prep
%setup -q -n findlib

%build
./configure \
	-bindir %{_bindir} \
	-mandir %{_mandir} \
	-config %{_sysconfdir}/ocamlfind.conf

%{__make} all opt

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install PREFIX=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib/*.mli

#doc/QUICKSTART is also in html
gzip -9nf README LICENSE TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz doc/html
%attr(755,root,root) %{_bindir}/*
%{_libdir}/ocaml/findlib
%{_libdir}/ocaml/site-lib
%config %{_sysconfdir}/ocamlfind.conf
%{_mandir}/man*/*
