# c6e
Repo of info for conary and centos 6 

conary on centos 6 from scratch
-------------------------------

Not for the weak
=================

## Enable EPEL

```sh
yum install --enablerepo=extras epel-release
```

## Dependencies

```sh
yum install python-lxml python-epdb python-crypto m2crypto python-kid libxslt
```

## Dependencies for devel purposes only

```sh
yum install openssl-devel zlib-devel elfutils-libelf-devel python-devel gcc make automake procps rpmdevtools
```

## Build an rpm

These instructions are for conary-2.5.5 we can update it after machine is assimilated.

Use rpmdevtools to create your rpmbuild tree.

```sh
rpmdev-setuptree
```

### Get the sources

```sh
mkdir -p ~/git/github

cd ~/git/github

git clone https://github.com/sassoftware/conary.git

cd conary

git archive --prefix=conary-2.5.5/ conary-2.5.5 | gzip > ~/rpmbuild/SOURCES/conary-2.5.5.tar.gz

(cd ~/rpmbuild/SOURCES && curl -O http://sqlite.org/sqlite-autoconf-3071201.tar.gz)
```

### Time to build

```sh
cp ~/git/github/c6e/conary/specs/conary.spec ~/rpmbuild/SPECS/

cp ~/git/github/c6e/conary/patches/*.patch ~/rpmbuild/SOURCES/

cd ~/rpmbuild/SPECS

rpmbuild -ba conary.spec
```

## Install the rpms

```sh
rpm -ivh ~/rpmbuild/RPMS/x86_64/conary-*.x86_64.rpm
```

## Create configs

conaryrc

```bash
cat > .conaryrc << EOF
name Anonymous
contact <user>@email.com

installLabelPath epel.cny.sas.com@sas:epel-6e centos6.rpath.com@rpath:centos-6-common centos6.rpath.com@rpath:centos-6e

buildLabel foo@bar:f

repositoryMap *.rpath.com https://updates.sas.com/conary
repositoryMap *.sas.com https://updates.sas.com/conary

autoLoadRecipes group-superclasses=centos6.rpath.com@rpath:centos-6-common

[x86_64]
buildFlavor is: x86_64
flavor is: x86_64
flavor is: x86

EOF
```

```bash
touch base.system-model

MODEL='group-epel-packages=epel.cny.sas.com@sas:epel-6e group-rpath-packages=centos6.rpath.com@rpath:centos-6-common group-os=centos6.rpath.com@rpath:centos-6e'

for i in $MODEL;
    do
        GRP=$(conary rq $i --labels --flavors)
        echo -en "search '${GRP}'\n" >> base.system-model
done

echo -en "\ninstall group-standard\nisntall group-rpath-core\n" >> base.system-model

cp -v base.system-model /etc/conary/system-model

```

Run following to finish assimilation

```bash
conary sync --replace-unmanaged-files --replace-managed-files

```
