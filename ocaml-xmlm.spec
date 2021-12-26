# TODO: odoc
#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	xmlm
%define		debug_package	%{nil}
Summary:	OCaml XML manipulation module
Summary(pl.UTF-8):	Moduł OCamla do operacji na XML-u
Name:		ocaml-%{module}
Version:	1.3.0
Release:	1
License:	ISC
Group:		Libraries
Source0:	https://erratique.ch/software/xmlm/releases/%{module}-%{version}.tbz
# Source0-md5:	d63ce15d913975211196b5079e86a797
URL:		https://erratique.ch/software/xmlm
BuildRequires:	ocaml >= 1:4.02.0
BuildRequires:	ocaml-topkg >= 0.9.0
BuildRequires:	ocaml-findlib-devel >= 1.4
BuildRequires:	ocaml-ocamlbuild
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xmlm allows the OCaml programmer to manipulate XML data. Its
complexity is half-way between the easy xml-light module and a full
parsing of XML data. It is also very simple to upgrade existing code
using xml-light in order to use xmlm.

%description -l pl.UTF-8
Xmlm pozwala programistom OCamla operować na danych XML. Złożoność tej
biblioteki mieści się między łatwym modulem xml-light, a pełną analizą
danych XML. Bardzo proste jest też przeniesienie istniejącego kodu
wykorzystującego xml-light, aby używał xmlm.

%package devel
Summary:	xmlm binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania xmlm dla OCamla - cześć programistyczna
Group:		Development/Libraries
%requires_eq	ocaml

%description devel
This package contains all the development stuff you need to develop
OCaml programs which use xmlm.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki xmlm.

%prep
%setup -q -n %{module}-%{version}

%build
ocaml pkg/pkg.ml build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}

cp -p _build/pkg/META _build/opam $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}
cp -p _build/src/*.{cma,cmi,cmt,cmti,mli} $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}
%if %{with ocaml_opt}
cp -p _build/src/*.{a,cmxs,cmx,cmxa} $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.md
%dir %{_libdir}/ocaml/xmlm
%{_libdir}/ocaml/xmlm/META
%{_libdir}/ocaml/xmlm/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/xmlm/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%doc src/*.mli
%{_libdir}/ocaml/xmlm/*.cmi
%{_libdir}/ocaml/xmlm/*.cmt
%{_libdir}/ocaml/xmlm/*.cmti
%{_libdir}/ocaml/xmlm/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/xmlm/*.cmx
%{_libdir}/ocaml/xmlm/*.cmxa
%{_libdir}/ocaml/xmlm/*.a
%endif
%{_libdir}/ocaml/xmlm/opam
