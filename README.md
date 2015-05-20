# c6e
Repo of info for conary and centos 6 

conary on centos 6 from scratch
-------------------------------

Not for the weak
=================

## Enable EPEL

yum install --enablerepo=extras epel-release

## Dependencies

yum install python-lxml python-epdb python-crypto m2crypto python-kid libxslt

## Dependencies for devel purposes only

yum install openssl-devel zlib-devel elfutils-libelf-devel python-devel gcc make automake procps rpmdevtools


## Build an rpm

These instructions are for conary-2.5.5 we can update it after machine is assimilated.

Use rpmdevtools to create your rpmbuild tree.

`rpmdev-setuptree`

### Get the sources

`mkdir -p ~/git/github`

`cd ~/git/github`

`git clone https://github.com/sassoftware/conary.git`

`cd conary`

`git archive --prefix=conary-2.5.5/ conary-2.5.5 | gzip > ~/rpmbuild/SOURCES/conary-2.5.5.tar.gz`

`(cd ~/rpmbuild/SOURCES && curl -O http://sqlite.org/sqlite-autoconf-3071201.tar.gz)`

### Time to build

`cp ~/git/github/c6e/conary/specs/conary.spec ~/rpmbuild/SPECS/`

`cp ~/git/github/c6e/conary/patches/*.patch ~/rpmbuild/SOURCES/`

`cd ~/rpmbuild/SPECS`

`rpmbuild -ba conary.spec`

## Install the rpms

`rpm -ivh ~/rpmbuild/RPMS/x86_64/conary-*.x86_64.rpm`

