#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Embedded Linux Library
Summary(pl.UTF-8):	Embedded Linux Library - biblioteka osadzonego Linuksa
Name:		ell
Version:	0.76
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://www.kernel.org/pub/linux/libs/ell/%{name}-%{version}.tar.xz
# Source0-md5:	5955fa2d683b5e159a1acbd0046d8a95
URL:		https://git.kernel.org/pub/scm/libs/ell/ell.git/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	libtool >= 2:2.2
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Embedded Linux Library.

%description -l pl.UTF-8
Embedded Linux Library - biblioteka osadzonego Linuksa.

%package devel
Summary:	Header files for ELL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ELL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for ELL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ELL.

%package static
Summary:	Static ELL library
Summary(pl.UTF-8):	Statyczna biblioteka ELL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ELL library.

%description static -l pl.UTF-8
Statyczna biblioteka ELL.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I build-aux
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-pie \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libell.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libell.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libell.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libell.so
%{_includedir}/ell
%{_pkgconfigdir}/ell.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libell.a
%endif
