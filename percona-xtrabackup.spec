Name: percona-xtrabackup
Summary: Online backup for InnoDB/XtraDB in MySQL, Percona Server and MariaDB
Version: 2.3.6
Release: 1
License: GPLv2
URL: http://www.percona.com/software/percona-xtrabackup/
Source: percona-xtrabackup-%{version}.tar.gz
Patch1: gcc-7-flags-fix.patch
Patch2: compilec-fix.patch

Provides: %{name}

BuildRequires: automake
BuildRequires: cmake >= 2.6.3
BuildRequires: patch
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libtool

BuildRequires: perl-generators
BuildRequires: procps
BuildRequires: python-sphinx

BuildRequires: vim-common
BuildRequires: bison
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: libaio-devel
BuildRequires: libgcrypt-devel
BuildRequires: libcurl-devel
BuildRequires: libev-devel
Requires: perl(DBD::mysql)
Requires: libcurl
Requires: libev

%description
Online backup for InnoDB/XtraDB in MySQL, MariaDB and Percona Server.

%package test
Summary: Test suite for Percona Xtrabackup
Provides: %{name}-test
Requires: %{name}
Requires: /usr/bin/mysql
Requires: %{name} = %{version}-%{release}

%description test
This package contains the test suite for Percona Xtrabackup

%prep
%setup -qn %{name}-%{name}-%{version}
%patch1 -p1
%patch2 -p1

%build
cmake -DBUILD_CONFIG=xtrabackup_release && make %{?_smp_mflags}

%install
[ "%{buildroot}" != '/' ] && rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_mandir}/man1
# install binaries and configs

SRC_DIR=storage/innobase/xtrabackup/src
pushd .
cd $SRC_DIR
install -p -m 755 xtrabackup %{buildroot}%{_bindir}
ln -sf xtrabackup %{buildroot}%{_bindir}/innobackupex
install -p -m 755 xbstream %{buildroot}%{_bindir}
install -p -m 755 xbcrypt %{buildroot}%{_bindir}
cd ..
find test -size 0 -delete
cp -pR test %{buildroot}%{_datadir}/percona-xtrabackup-test
rm -rf %{buildroot}%{_datadir}/percona-xtrabackup-test/kewpie
rm -rf %{buildroot}%{_datadir}/percona-xtrabackup-test/*Make*
cd doc/source/build/man
install -m 644 *.1 %{buildroot}%{_mandir}/man1

popd

%files
%{_bindir}/innobackupex
%{_bindir}/xtrabackup
%{_bindir}/xbstream
%{_bindir}/xbcrypt
%doc COPYING README VERSION
%{_mandir}/man1/innobackupex.1.gz
%{_mandir}/man1/xtrabackup.1.gz
%{_mandir}/man1/xbstream.1.gz
%{_mandir}/man1/xbcrypt.1.gz

%files -n percona-xtrabackup-test
%{_datadir}/percona-xtrabackup-test
%doc COPYING

%changelog
* Mon Jul 26 2021 bzhaoop <bzhaojyathousandy@gmail.com> - 2.3.6-1
- Init project for percona-xtrabackup

