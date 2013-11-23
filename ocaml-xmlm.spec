#
# Conditional build:
%bcond_without	opt		# build opt

%define		pkgname	xmlm
%define		debug_package	%{nil}
Summary:	OCaml xml manipulation module
Name:		ocaml-%{pkgname}
Version:	1.1.1
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://erratique.ch/software/xmlm/releases/%{pkgname}-%{version}.tbz
# Source0-md5:	357025dd1a9fc87b6e50ac21eb0eb2b1
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
#Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains all the development stuff you need to develop
OCaml programs which use xmlm.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n %{pkgname}-%{version}

%build
ocaml setup.ml -configure
ocaml setup.ml -build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{xmlm,stublibs}
install _build/src/*.cm[ixa]* _build/src/*.a $RPM_BUILD_ROOT%{_libdir}/ocaml/xmlm

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/xmlm
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/xmlm/META <<EOF
requires = ""
version = "%{version}"
directory = "+xmlm"
archive(byte) = "xmlm.cma"
archive(native) = "xmlm.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc README CHANGES src/*.mli
%dir %{_libdir}/ocaml/xmlm
%{_libdir}/ocaml/xmlm/*.cm[ixa]*
%{_libdir}/ocaml/xmlm/*.a
%{_libdir}/ocaml/site-lib/xmlm
