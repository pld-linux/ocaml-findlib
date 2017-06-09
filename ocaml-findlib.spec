#
# Conditional build:
%bcond_without	ocaml_opt		# build opt
%bcond_without	tk      		# build without tk support

%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		ocaml_ver	1:4.04
Summary:	OCaml module manager
Summary(pl.UTF-8):	Zarządca modułów OCamla
Name:		ocaml-findlib
Version:	1.7.3
Release:	1
License:	distributable
Group:		Development/Tools
Source0:	http://download.camlcity.org/download/findlib-%{version}.tar.gz
# Source0-md5:	7d57451218359f7b7dfc969e3684a6da
Patch0:		%{name}-bytes.patch
URL:		http://www.ocaml-programming.de/packages/
BuildRequires:	m4
BuildRequires:	ncurses-devel
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-camlp4
%{?with_tk:BuildRequires:	ocaml-labltk-devel}
BuildRequires:	sed >= 4.0
%requires_eq	ocaml
Conflicts:	ocaml-curses < 1.0.3-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without ocaml_opt}
%define		no_install_post_strip	1
# debug package strips binaries which renders ocamlfind broken
%define		_enable_debug_packages	0
%endif

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

%{__make} -j1 all %{?with_ocaml_opt:opt}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/findlib/*.mli

# now provided by ocaml-dbm.spec (might not exist if building without ocaml-dbm installed)
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/dbm
# now provided by ocaml-labltk.spec (might not exist if building without ocaml-labltk installed)
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/labltk
# now provided by ocaml-ocamlbuild.spec (might not exist if building without ocaml-ocamlbuild installed)
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ocamlbuild

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

%pretrans
# handle ocaml-findlib-1.6.2-{2,3} + ocaml-curses < 1.0.3-13 mess
[ -L %{_libdir}/ocaml/site-lib/libexec ] || rmdir %{_libdir}/ocaml/site-lib/libexec || :
[ -L %{_libdir}/ocaml/site-lib/stublibs ] || rmdir %{_libdir}/ocaml/site-lib/stublibs || :

%files
%defattr(644,root,root,755)
%doc doc/README LICENSE doc/*-html
%attr(755,root,root) %{_bindir}/ocamlfind
%attr(755,root,root) %{_bindir}/safe_camlp4
%config %{_sysconfdir}/ocamlfind.conf
%dir %{_libdir}/ocaml/findlib
%if %{with tk}
%attr(755,root,root) %{_libdir}/ocaml/findlib/make_wizard
%{_libdir}/ocaml/findlib/make_wizard.pattern
%endif
%{_libdir}/ocaml/findlib/Makefile.config
%{_libdir}/ocaml/findlib/findlib.cma
%{_libdir}/ocaml/findlib/findlib_dynload.cma
%{_libdir}/ocaml/findlib/findlib_top.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/findlib/findlib.cmxs
%attr(755,root,root) %{_libdir}/ocaml/findlib/findlib_dynload.cmxs
%attr(755,root,root) %{_libdir}/ocaml/findlib/findlib_top.cmxs
%endif
%{_libdir}/ocaml/site-lib/findlib
# symlinks
%{_libdir}/ocaml/site-lib/libexec
%{_libdir}/ocaml/site-lib/stublibs
# META files for base ocaml packages
%{_libdir}/ocaml/site-lib/bigarray
%{_libdir}/ocaml/site-lib/bytes
%{_libdir}/ocaml/site-lib/compiler-libs
%{_libdir}/ocaml/site-lib/dynlink
%{_libdir}/ocaml/site-lib/graphics
%{_libdir}/ocaml/site-lib/num
%{_libdir}/ocaml/site-lib/num-top
%{_libdir}/ocaml/site-lib/ocamldoc
%ifarch %{x8664}
%{_libdir}/ocaml/site-lib/raw_spacetime
%endif
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
%{_libdir}/ocaml/findlib/findlib.cmi
%{_libdir}/ocaml/findlib/fl_*.cmi
%{_libdir}/ocaml/findlib/topfind.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/findlib/findlib.a
%{_libdir}/ocaml/findlib/findlib.cmxa
%{_libdir}/ocaml/findlib/findlib_dynload.a
%{_libdir}/ocaml/findlib/findlib_dynload.cmxa
%{_libdir}/ocaml/findlib/findlib_top.a
%{_libdir}/ocaml/findlib/findlib_top.cmxa
%endif
%dir %{_libdir}/ocaml/num-top
%{_libdir}/ocaml/num-top/num_top.cma
%{_libdir}/ocaml/num-top/num_top*.cmi
%{_libdir}/ocaml/ocamlfind
%{_libdir}/ocaml/topfind
