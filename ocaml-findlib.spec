%define		ocaml_ver	1:4.02
Summary:	OCaml module manager
Summary(pl.UTF-8):	Zarządca modułów OCamla
Name:		ocaml-findlib
Version:	1.5.5
Release:	1
License:	distributable
Group:		Development/Tools
Source0:	http://download.camlcity.org/download/findlib-%{version}.tar.gz
# Source0-md5:	703eae112f9e912507c3a2f8d8c48498
Patch0:		%{name}-bytes.patch
URL:		http://www.ocaml-programming.de/packages/
BuildRequires:	m4
BuildRequires:	ncurses-devel
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-labltk
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
%patch0 -p1

%build
./configure \
	-bindir %{_bindir} \
	-mandir %{_mandir} \
	-config %{_sysconfdir}/ocamlfind.conf \
	-with-toolbox

sed -i -e 's/-g//' Makefile

%{__make} -j1 all opt

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib/*.mli

# now provided by ocaml-labltk.spec
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/labltk
# now provided by ocaml-dbm.spec (might not exist if building without ocaml-dbm installed)
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/dbm

# in PLD only META files are stored in site-lib/pkg
sed -i -e 's|/site-lib||' $RPM_BUILD_ROOT%{_libdir}/ocaml/topfind
ln -sf topfind $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlfind
%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/findlib
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib
%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/findlib/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib
echo 'directory = "+findlib"' >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib/META
%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/num-top \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/num-top
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/num-top
%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/num-top/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/num-top
echo 'directory = "+findlib"' >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/num-top/META

echo 'ldconf = "ignore"' >> $RPM_BUILD_ROOT%{_sysconfdir}/ocamlfind.conf

ln -sf ../stublibs $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/libexec
ln -sf ../stublibs $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/stublibs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/README LICENSE doc/*-html
%attr(755,root,root) %{_bindir}/ocamlfind
%attr(755,root,root) %{_bindir}/safe_camlp4
%config %{_sysconfdir}/ocamlfind.conf
%dir %{_libdir}/ocaml/findlib
%attr(755,root,root) %{_libdir}/ocaml/findlib/make_wizard
%{_libdir}/ocaml/findlib/make_wizard.pattern
%{_libdir}/ocaml/site-lib/findlib
# symlinks
%{_libdir}/ocaml/site-lib/libexec
%{_libdir}/ocaml/site-lib/stublibs
# META files for base ocaml packages
%{_libdir}/ocaml/site-lib/bigarray
%{_libdir}/ocaml/site-lib/bytes
%{_libdir}/ocaml/site-lib/compiler-libs/META
%{_libdir}/ocaml/site-lib/dynlink
%{_libdir}/ocaml/site-lib/graphics
%{_libdir}/ocaml/site-lib/num
%{_libdir}/ocaml/site-lib/num-top
%{_libdir}/ocaml/site-lib/ocamlbuild
%{_libdir}/ocaml/site-lib/stdlib
%{_libdir}/ocaml/site-lib/str
%{_libdir}/ocaml/site-lib/threads
%{_libdir}/ocaml/site-lib/unix
# camlp4 4.02 doesn't provide its META itself
%{_libdir}/ocaml/site-lib/camlp4
%{_mandir}/man1/ocamlfind.1*
%{_mandir}/man5/META.5*
%{_mandir}/man5/findlib.conf.5*
%{_mandir}/man5/site-lib.5*

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/findlib/Makefile.config
%{_libdir}/ocaml/findlib/*.cm[ixa]*
%{_libdir}/ocaml/findlib/*.a
%dir %{_libdir}/ocaml/num-top
%{_libdir}/ocaml/num-top/*.cm[ia]
%{_libdir}/ocaml/ocamlfind
%{_libdir}/ocaml/topfind
