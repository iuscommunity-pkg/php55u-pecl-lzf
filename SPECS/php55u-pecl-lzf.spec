%define pecl_name LZF
%define real_name php-pecl-lzf
%define php_base php55u
%global ini_name 40-lzf.ini

Name: %{php_base}-pecl-lzf
Version: 1.6.3
Release: 2.ius%{?dist}
Summary: Extension to handle LZF de/compression
Group: Development/Languages
License: PHP
URL: http://pecl.php.net/package/%{pecl_name}
Source0: http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRequires: %{php_base}-devel
BuildRequires: %{php_base}-pear >= 1:1.4.0
BuildRequires: liblzf-devel

Requires: %{php_base}(zend-abi) = %{php_zend_api}
Requires: %{php_base}(api) = %{php_core_api}

Requires(post): %{php_base}-pear
Requires(postun): %{php_base}-pear

# provide the stock name
Provides: %{real_name} = %{version}
Provides: %{real_name}%{?_isa} = %{version}

# provide the stock and IUS names without pecl
Provides: php-%{pecl_name} = %{version}
Provides: php-%{pecl_name}%{?_isa} = %{version}
Provides: %{php_base}-%{pecl_name} = %{version}
Provides: %{php_base}-%{pecl_name}%{?_isa} = %{version}

# provide the stock and IUS names in pecl() format
Provides: php-pecl(%{pecl_name}) = %{version}
Provides: php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides: %{php_base}-pecl(%{pecl_name}) = %{version}
Provides: %{php_base}-pecl(%{pecl_name})%{?_isa} = %{version}

# conflict with the stock name
Conflicts: %{real_name} < %{version}

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
# remove bundled lzf libs
%{__rm} -rf %{pecl_name}-%{version}/libs


%build
cd %{pecl_name}-%{version}
phpize
%configure --with-liblzf --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}


%install
pushd %{pecl_name}-%{version}
%{__make} install INSTALL_ROOT=%{buildroot}

%{__mkdir_p} %{buildroot}%{php_inidir}
%{__cat} > %{buildroot}%{php_inidir}/%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=lzf.so
EOF
popd

%{__install} -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml


%check
cd %{pecl_name}-%{version}

TEST_PHP_EXECUTABLE=%{_bindir}/php \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{_bindir}/php run-tests.php \
    -n -q \
    -d extension_dir=%{buildroot}%{php_extdir} \
    -d extension=lzf.so \


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%doc %{pecl_name}-%{version}/CREDITS
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/lzf.so
%{pecl_xmldir}/%{pecl_name}.xml


%changelog
* Thu Mar 17 2016 Carl George <carl.george@rackspace.com> - 1.6.3-2.ius
- Clean up provides
- Clean up filters
- Install package.xml as %%{pecl_name}.xml, not %%{name}.xml
- Use same configure and make commands as Fedora

* Tue Apr 21 2015 Carl George <carl.george@rackspace.com> - 1.6.3-1.ius
- Latest upstream
- Remove patch0
- Delete bundled libs in %%prep and use --with-liblzf flag

* Wed Oct 15 2014 Carl George <carl.george@rackspace.com> - 1.6.2-10.ius
- Conflict with the correct version

* Fri Oct 10 2014 Carl George <carl.george@rackspace.com> - 1.6.2-9.ius
- Directly require the correct pear package, not /usr/bin/pecl
- Use same provides as stock package

* Mon Oct 06 2014 Carl George <carl.george@rackspace.com> - 1.6.2-8.ius
- Add numerical prefix to extension configuration file

* Thu Nov 07 2013 Ben Harper <ben.harper@rackspace.com> - 1.6.2-7.ius
- adding provides per LB bug 1249003

* Mon Oct 28 2013 Mark McKinstry <mmckinst@nexcess.net> - 1.6.2-6.ius
- build IUS RPM from 1.6.2-5 from f20
- add ius suffix to release
- clean up spec some

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.6.2-4
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 28 2012 Andrew Colin Kissa - 1.6.2-2
- Fix php spec macros
- Fix Zend API version checks

* Sat Oct 20 2012 Andrew Colin Kissa - 1.6.2-1
- Upgrade to latest upstream
- Fix bugzilla #838309 #680230

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.5.2-9
- rebuild against PHP 5.4, with upstream patch
- add filter to avoid private-shared-object-provides
- add minimal %%check

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-7
- Fix bugzilla #715791

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.5.2-4
- rebuild for new PHP 5.3.0 ABI (20090626)

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-3
- Consistent use of macros

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-2
- Fixes to the install to retain timestamps and other fixes raised in review

* Sun Jun 14 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-1
- Initial RPM package
