#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	xmlm
%define		debug_package	%{nil}
Summary:	OCaml xml manipulation module
Name:		ocaml-%{module}
Version:	1.2.0
Release:	5
License:	BSD
Group:		Libraries
Source0:	http://erratique.ch/software/xmlm/releases/%{module}-%{version}.tbz
# Source0-md5:	7e6d3363c2395d84274f1b480e4b6003
URL:		http://erratique.ch/software/xmlm
BuildRequires:	ocaml >= 3.10
BuildRequires:	ocaml-findlib >= 1.4
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xmlm allows the OCaml programmer to manipulate xml data. Its
complexity is half-way between the easy xml-light module and a full
parsing of xml data. It is also very simple to updgrade existing code
using xml-light in order to use xmlm.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	xmlm binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania xmlm dla OCamla - cześć programistyczna
Group:		Development/Libraries
%requires_eq	ocaml

%description devel
This package contains all the development stuff you need to develop
OCaml programs which use xmlm.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n %{module}-%{version}

%build
./pkg/build %{?with_ocaml_opt:true} %{!?with_ocaml_opt:false}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{%{module},stublibs}
install _build/src/*.cm[ixa]* %{?with_ocaml_opt:_build/src/*.a} $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META <<EOF
requires = ""
version = "%{version}"
directory = "+%{module}"
archive(byte) = "%{module}.cma"
archive(native) = "%{module}.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc README.md CHANGES.md src/*.mli
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/*.cma
%{_libdir}/ocaml/%{module}/*.cm[ix]
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.cmxa
%{_libdir}/ocaml/%{module}/*.a
%endif
%{_libdir}/ocaml/site-lib/%{module}
