#
# Conditional build:
%bcond_without	ocaml_opt		# build opt
%bcond_without	tk			# build without tk support

%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		ocaml_ver	1:4.04
Summary:	OCaml module manager
Summary(pl.UTF-8):	Zarządca modułów OCamla
Name:		ocaml-findlib
Version:	1.9.1
Release:	2
License:	distributable
Group:		Development/Tools
Source0:	http://download.camlcity.org/download/findlib-%{version}.tar.gz
# Source0-md5:	65e6dc9b305ccbed1267275fe180f538
Patch0:		labltk.patch
URL:		http://projects.camlcity.org/projects/findlib.html
BuildRequires:	m4
BuildRequires:	ncurses-devel
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-camlp4
%{?with_tk:BuildRequires:	ocaml-labltk-devel}
BuildRequires:	ocaml-ocamldoc-devel
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
	-sitelib %{_libdir}/ocaml \
	-with-toolbox

sed -i -e 's/-g//' Makefile

%{__make} -j1 all %{?with_ocaml_opt:opt}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/findlib/*.mli

# now provided by ocaml-dbm.spec (might not exist if building without ocaml-dbm installed)
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/dbm
# now provided by ocaml-labltk.spec (might not exist if building without ocaml-labltk installed)
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk
# now provided by ocaml-ocamlbuild.spec (might not exist if building without ocaml-ocamlbuild installed)
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlbuild

ln -sf topfind $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlfind

echo 'ldconf = "ignore"' >> $RPM_BUILD_ROOT%{_sysconfdir}/ocamlfind.conf

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_libdir}/ocaml/findlib/Makefile.packages
%{_libdir}/ocaml/findlib/findlib.cma
%{_libdir}/ocaml/findlib/findlib_dynload.cma
%{_libdir}/ocaml/findlib/findlib_top.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/findlib/findlib.cmxs
%attr(755,root,root) %{_libdir}/ocaml/findlib/findlib_dynload.cmxs
%attr(755,root,root) %{_libdir}/ocaml/findlib/findlib_top.cmxs
%endif
%{_libdir}/ocaml/findlib
# META files for base ocaml packages
%{_libdir}/ocaml/bigarray
%{_libdir}/ocaml/bytes
%{_libdir}/ocaml/compiler-libs
%{_libdir}/ocaml/dynlink
%{_libdir}/ocaml/ocamldoc
%{_libdir}/ocaml/stdlib
%{_libdir}/ocaml/str
%{_libdir}/ocaml/threads
%{_libdir}/ocaml/unix
# camlp4 4.02 doesn't provide its META itself
%{_libdir}/ocaml/camlp4
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
%{_libdir}/ocaml/ocamlfind
%{_libdir}/ocaml/topfind
