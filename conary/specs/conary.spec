%define _py_ver 2.6
%if 0%{?fedora} >= 20
%define _py_ver 2.7
%endif

%if 0%{?centos} >= 7
%define _py_ver 2.7
%endif

%define _instdir            /

%if 0%{?_instdir:1} 
%define _prefix            %{_instdir}/usr
%define _sysconfdir        %{_instdir}/etc
%define _sharedstatedir    %{_instdir}/var/lib
%define _infodir           %{_datadir}/info
%define _mandir            %{_datadir}/man
%define _localstatedir     %{_instdir}/var
%endif

Name: conary          
Version: 2.5.5 
Release: 1%{?dist}
Summary: Conary Package Manager       
License: Apache 2.0     
URL: https://github.com/sassoftware/conary            
Source0: https://github.com/sassoftware/conary/archive/%name-%version.tar.gz  
Source1: http://sqlite.org/sqlite-autoconf-3071201.tar.gz
#Source2: https://raw.githubusercontent.com/sassoftware/conary/master/recipes/unified/conary/el5-build-flags.patch

Patch0: el5-build-flags.patch
Patch1: %name-%version-rpm2cpio.patch
Patch2: %name-%version-makefiles.patch

BuildRequires: python-lxml python-epdb rpm-libs rpm-python openssl-devel python-crypto m2crypto zlib-devel elfutils-libelf-devel python-devel python-kid 
Requires: rpm-libs rpm-python openssl python-crypto m2crypto     
Buildroot: %{_tmppath}/%{name}-buildroot
Packager: Brett Smith <bc.smith@sas.com>

%description 
Conary is a software configuration manager that uses distributed,
network-based, versioned repositories rather than disparate package
files as its canonical source of data.  Conary uses the repository
versioning to intelligently merge configuration files, file ownership
and permissions, and so forth.

%package build
Summary: Build commands for conary 

%description build
Conary build tools for Build Management. Includes the Conary version control program, called cvc, handles build and source management, and is  responsible  for  all changes to the repository.

%package repository
Summary: Repository code for conary
Requires: python-lxml python-kid
%description repository
Conary software for installing, configuring, and managing a Conary Repository. A Conary repository is a network-accessible software repository at the heart of Conary's version control features. Conary runs as a service rather than as a data store like APT and YUM repositories. 

%prep
%setup -q 

patch -p1 < %{_builddir}/%{name}-%{version}/recipes/unified/conary/el5-build-flags.patch
%patch1 -p1
%patch2 -p1
 
CFLAGS="$CFLAGS -fPIC" 

cd %{_builddir}/%{name}-%{version}/conary/pysqlite3/
tar -zxvf %{_sourcedir}/sqlite-autoconf-3071201.tar.gz
cd sqlite-autoconf-3071201
%configure --disable-shared --enable-threadsafe
make 

%build

#CXXFLAGS="-O2 -g -D_FORTIFY_SOURCE=2 -fstack-protector " CPPFLAGS="" CLASSPATH=""  LDFLAGS="-g -O1 " CC=gcc CXX=g++ CFLAGS="-O2 -g -D_FORTIFY_SOURCE=2 -fstack-protector -fPIC"  
LDFLAGS="$LDFLAGS -L%{_libdir} -Wl,-rpath,%{_libdir}"

PYINCLUDE=/usr/include/python%{_py_ver} PYTHON=/usr/bin/python%{_py_ver} PYVER=%{_py_ver} install_dir=%{_instdir} prefix=%{_prefix} bindir=%{_bindir} datadir=%{_datadir} libelf=-lelf make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
#CXXFLAGS="-O2 -g -D_FORTIFY_SOURCE=2 -fstack-protector " CPPFLAGS="" CLASSPATH=""  LDFLAGS="-g -O1 " CC=gcc CXX=g++ CFLAGS="-O2 -g -D_FORTIFY_SOURCE=2 -fstack-protector -fPIC"  
PYINCLUDE=/usr/include/python%{_py_ver} PYTHON=/usr/bin/python%{_py_ver} PYVER=%{_py_ver} install_dir=%{_instdir} prefix=%{_prefix} bindir=%{_bindir} datadir=%{_datadir} libelf=-lelf %make_install


%files
%{_sysconfdir}/conary-repos/*
%{_sysconfdir}/conary/*
%{_sysconfdir}/logrotate.d/conary-repos.conf
%{_sysconfdir}/nginx/conf.d/conary-common.conf
%{_sysconfdir}/sysconfig/conary-repos
%{_bindir}/ccs2tar
%{_bindir}/conary
%{_bindir}/conary-debug
%{_bindir}/dbsh
%{_libdir}/conary/*
%{_mandir}/man1/conary.*
%{_datadir}/conary/dumpcontainer
%{_datadir}/conary/genmodel
%{_datadir}/conary/hashpassword
%{_datadir}/conary/listcachedir
%{_datadir}/conary/localupdateinfo
%{_datadir}/conary/md5pw
%{_datadir}/conary/mirror
%{_datadir}/conary/promote-redirects
%{_datadir}/conary/recreatedb
%{_datadir}/conary/showchangeset
%{_libdir}/python%{_py_ver}/site-packages/conary/__init__.*
%{_libdir}/python%{_py_ver}/site-packages/conary/_sqlite3.*
%{_libdir}/python%{_py_ver}/site-packages/conary/build/__init__.*
%{_libdir}/python%{_py_ver}/site-packages/conary/build/errors.*
%{_libdir}/python%{_py_ver}/site-packages/conary/build/filter.*
%{_libdir}/python%{_py_ver}/site-packages/conary/build/nextversion.*
%{_libdir}/python%{_py_ver}/site-packages/conary/build/tags.*
%{_libdir}/python%{_py_ver}/site-packages/conary/build/use.*
%{_libdir}/python%{_py_ver}/site-packages/conary/callbacks.*
%{_libdir}/python%{_py_ver}/site-packages/conary/changelog.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/__init__.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/commit.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/conarycmd.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/cscmd.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/fmtroves.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/metadata.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/query.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/queryrep.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/rollbacks.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/search.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/showchangeset.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/updatecmd.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/verify.*
%{_libdir}/python%{_py_ver}/site-packages/conary/command.*
%{_libdir}/python%{_py_ver}/site-packages/conary/commit.*
%{_libdir}/python%{_py_ver}/site-packages/conary/commitaction
%{_libdir}/python%{_py_ver}/site-packages/conary/conarycfg.*
%{_libdir}/python%{_py_ver}/site-packages/conary/conaryclient/*
%{_libdir}/python%{_py_ver}/site-packages/conary/constants.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cscmd.*
%{_libdir}/python%{_py_ver}/site-packages/conary/dbstore/*
%{_libdir}/python%{_py_ver}/site-packages/conary/deps/*
%{_libdir}/python%{_py_ver}/site-packages/conary/display.*
%{_libdir}/python%{_py_ver}/site-packages/conary/errors.*
%{_libdir}/python%{_py_ver}/site-packages/conary/files.*
%{_libdir}/python%{_py_ver}/site-packages/conary/flavorcfg.*
%{_libdir}/python%{_py_ver}/site-packages/conary/fmtroves.*
%{_libdir}/python%{_py_ver}/site-packages/conary/keymgmt.*
%{_libdir}/python%{_py_ver}/site-packages/conary/lib/*
%{_libdir}/python%{_py_ver}/site-packages/conary/local/*
%{_libdir}/python%{_py_ver}/site-packages/conary/metadata.*
%{_libdir}/python%{_py_ver}/site-packages/conary/pysqlite3-0.0.0-py%{_py_ver}.egg-info
%{_libdir}/python%{_py_ver}/site-packages/conary/query.*
%{_libdir}/python%{_py_ver}/site-packages/conary/queryrep.*
%{_libdir}/python%{_py_ver}/site-packages/conary/repository/*.py*
%{_libdir}/python%{_py_ver}/site-packages/conary/rollbacks.*
%{_libdir}/python%{_py_ver}/site-packages/conary/rpmhelper.*
%{_libdir}/python%{_py_ver}/site-packages/conary/showchangeset.*
%{_libdir}/python%{_py_ver}/site-packages/conary/sqlite3/__init__.*
%{_libdir}/python%{_py_ver}/site-packages/conary/sqlite3/main.*
%{_libdir}/python%{_py_ver}/site-packages/conary/state.*
%{_libdir}/python%{_py_ver}/site-packages/conary/streams.*
%{_libdir}/python%{_py_ver}/site-packages/conary/trove.*
%{_libdir}/python%{_py_ver}/site-packages/conary/trovetup.*
%{_libdir}/python%{_py_ver}/site-packages/conary/updatecmd.*
%{_libdir}/python%{_py_ver}/site-packages/conary/verify.*
%{_libdir}/python%{_py_ver}/site-packages/conary/versions.*

%docdir %{_instdir}%{_datadir}/doc
%doc LICENSE NEWS

%files build
%{_sysconfdir}/conary/mirrors/*
#%{_sysconfdir}/recipeTemplates/*
%{_libdir}/conary/ScanDeps/Module/ScanDeps.pm
%{_libdir}/conary/ScanDeps/Module/ScanDeps/DataFeed.pm
%{_libdir}/conary/filename_wrapper.so
%{_libdir}/python%{_py_ver}/site-packages/conary/branch.*
%{_libdir}/python%{_py_ver}/site-packages/conary/build/*
%{_libdir}/python%{_py_ver}/site-packages/conary/checkin.*
%{_libdir}/python%{_py_ver}/site-packages/conary/clone.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/branch.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/clone.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cmds/cvccmd.*
%{_libdir}/python%{_py_ver}/site-packages/conary/cvc.*
%{_bindir}/cvc
%{_libexecdir}/conary/perlreqs.pl
%{_mandir}/man1/cvc.*


%files repository
%{_datadir}/conary/logcat
%{_datadir}/conary/migration/*
%{_libdir}/python%{_py_ver}/site-packages/conary/changemail.*
%{_libdir}/python%{_py_ver}/site-packages/conary/logaction.*
%{_libdir}/python%{_py_ver}/site-packages/conary/repository/netrepos/*
%{_libdir}/python%{_py_ver}/site-packages/conary/server/*
%{_libdir}/python%{_py_ver}/site-packages/conary/web/*

%post
/sbin/ldconfig
%{_bindir}/conary q --config 'syncCapsuleDatabase false'


%changelog
* Tue Nov 18 2014 Brett Smith <bc.smith@sas.com> Update to 2.5.5 and turn off capsule sync 
* Mon Sep 26 2014 Brett Smith <bc.smith@sas.com> Patch Makefiles to build in alt locations
* Mon Aug 18 2014 Brett Smith <bc.smith@sas.com> Initial Build
- 
