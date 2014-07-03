Name:           js
Summary:        JavaScript interpreter
License:        MPL-1.1 or GPL-2.0+ or LGPL-2.1+
Group:          Development/Languages/Other
Version:        1.0.0
Release:        0
Url:            http://www.mozilla.org/js/
Source0:        http://ftp.mozilla.org/pub/mozilla.org/%{name}/%{name}-%{version}.tar.bz2
Source98:       baselibs.conf
BuildRequires:  autoconf213
BuildRequires:  gcc-c++
BuildRequires:  nspr-devel
BuildRequires:  pkg-config
BuildRequires:  python
BuildRequires:  zip
Provides:       mozjs185

%description
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
superset of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.

%package -n libmozjs185
Summary:        JavaScript library
Group:          System/Libraries

%description -n libmozjs185
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
superset of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.


%package devel
Summary:        Header files, libraries and development documentation for %{name}
Group:          Development/Libraries/Other
Requires:       libmozjs185 = %{version}-%{release}
Requires:       pkg-config
Provides:       libjs-devel = %{version}-%{release}
Provides:       mozjs185-devel

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n %{name}-%{version}

%build
export MOZILLA_VERSION=%{version}
cd js
pushd src
%configure --with-system-nspr --enable-threadsafe
popd
export BUILD_OPT=1
%{__make} %{?_smp_mflags} -C src \
	JS_THREADSAFE="1" \
	XCFLAGS="%{optflags} -fPIC " \
	BUILD_OPT="1" \

%install
cd js/src
%make_install
%{__rm} -rf %{buildroot}%{_libdir}/libmozjs185-1.0.a
# SO links are created wrong, fixing them
%{__rm} -rf %{buildroot}%{_libdir}/libmozjs185.so.1.0
%{__rm} -rf %{buildroot}%{_libdir}/libmozjs185.so
%{__ln_s} libmozjs185.so.1.0.0 %{buildroot}%{_libdir}/libmozjs185.so.1.0
%{__ln_s} libmozjs185.so.1.0.0 %{buildroot}%{_libdir}/libmozjs185.so
# JS shell
%{__install} -m 0755 shell/js %{buildroot}%{_bindir}/
# headers are installed with executable permissions
chmod 644 %{buildroot}%{_includedir}/js/*

%clean
%{__rm} -rf %{buildroot}

%post -n libmozjs185 -p /sbin/ldconfig

%postun -n libmozjs185 -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc js/src/README.html
%{_bindir}/js

%files -n libmozjs185
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
#%{_bindir}/jscpucfg
%{_bindir}/js-config
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/js/
