%global php_apiver	%((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:		%{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir:		%{expand: %%global php_extdir %(php-config --extension-dir)}}

%define pecl_name	LZF
%define real_name	php-pecl-lzf
%define php_base	php55u
%define basever		5.5

Name:		%{php_base}-pecl-lzf
Version:	1.6.2
Release:	1.ius%{?dist}
Summary:	Extension to handle LZF de/compression
Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/package/%{pecl_name}
Source0:	http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# remove bundled lzf libs
Patch0:		php-lzf-rm-bundled-libs.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	%{php_base}-devel
BuildRequires:	%{php_base}-pear >= 1:1.4.0
BuildRequires:	liblzf-devel
%if 0%{?php_zend_api:1}
Requires:	%{php_base}(zend-abi) = %{php_zend_api}
Requires:	%{php_base}(api) = %{php_core_api}
%else
# for EL-5
Requires:	%{php_base}-api = %{php_apiver}
%endif
Requires(post):	%{__pecl}
Requires(postun):	%{__pecl}
Provides:	%{php_base}-pecl(%{pecl_name}) = %{version}

Conflicts:	%{real_name} < %{basever}
Provides:	%{real_name} = %{version}-%{release}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%description
This extension provides LZF compression and decompression using the liblzf
library

LZF is a very fast compression algorithm, ideal for saving space with a 
slight speed cost.

%prep
%setup -c -q
%patch0 -p0

[ -f package2.xml ] || %{__mv} package.xml package2.xml
%{__mv} package2.xml %{pecl_name}-%{version}/%{pecl_name}.xml

%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}

%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot} INSTALL="install -p"

%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/lzf.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=lzf.so
EOF

%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -p -m 644 %{pecl_name}.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}

TEST_PHP_EXECUTABLE=%{_bindir}/php \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{_bindir}/php run-tests.php \
    -n -q \
    -d extension_dir=%{buildroot}%{php_extdir} \
    -d extension=lzf.so \


%clean
%{__rm} -rf %{buildroot}

%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/lzf.ini
%{php_extdir}/lzf.so
%{pecl_xmldir}/%{name}.xml

%changelog
* Thu Oct 28 2013 Mark McKinstry <mmckinst@nexcess.net> - 1.6.2-1.ius
- build RPM from 1.6.2-5 from f20
- add ius suffix to release
- clean up spec some
