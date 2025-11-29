#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	tests		# build tests
#
Summary:	Shared library for accessing MS Graph API
Summary(pl.UTF-8):	Biblioteka współdzielona do dostępu do MS Graph API
Name:		msgraph
Version:	0.2.3
Release:	2
License:	LGPL v3+
Group:		Libraries
Source0:	https://download.gnome.org/sources/msgraph/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	051f7353e6a2b30b5b893bcf6d7539fa
URL:		https://gitlab.gnome.org/GNOME/msgraph
BuildRequires:	gcc >= 6:4.7
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	gnome-online-accounts-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	json-glib-devel
BuildRequires:	librest-devel >= 0.9
BuildRequires:	libsoup3-devel >= 3.0
%{?with_tests:BuildRequires:	libxml2-devel}
BuildRequires:	meson >= 0.63.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
%{?with_tests:BuildRequires:	uhttpmock1-devel >= 0.11.0}
BuildRequires:	xz
Requires:	glib2 >= 1:2.28
Requires:	json-glib
Requires:	librest >= 0.9
Requires:	libsoup3 >= 3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmsgraph is a GLib-based library for accessing online service APIs
using MS Graph protocol.

%description -l pl.UTF-8
libmsgraph to oparta na GLib biblioteka służąca do dostępu do API
usług online wykorzystujących protokół MS Graph.

%package devel
Summary:	Header files for msgraph library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki msgraph
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.28
Requires:	gnome-online-accounts-devel
Requires:	json-glib-devel
Requires:	librest-devel >= 0.9
Requires:	libsoup3-devel >= 3.0

%description devel
Header files for msgraph library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki msgraph.

%package apidocs
Summary:	API documentation for msgraph library
Summary(pl.UTF-8):	Dokumentacja API biblioteki msgraph
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for msgraph library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki msgraph.

%prep
%setup -q

%build
%meson \
	%{!?with_apidocs:-Dgtk_doc=false} \
	-Dtests=%{__true_false tests}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/msgraph-0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_libdir}/libmsgraph-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmsgraph-0.so.1
%{_libdir}/girepository-1.0/Msg-0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmsgraph-0.so
%{_includedir}/msg
%{_datadir}/gir-1.0/Msg-0.gir
%{_pkgconfigdir}/msgraph-0.1.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/msgraph-0
%endif
