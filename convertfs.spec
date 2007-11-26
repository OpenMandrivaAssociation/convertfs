# OE: conditional switches
#(ie. use with rpm --rebuild):
#	--with diet	Compile convertfs against dietlibc

%define build_diet 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

%define name	convertfs
%define version 0.20020318
%define release 4mdk

Summary:	ConvertFS - convert one file system to another
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-18mar2002.tar.bz2
# lynx -dump -nolist http://tzukanov.narod.ru/convertfs/ > README
Source1:	README.bz2
License:	GPL
Group:		System/Kernel and hardware
URL:		http://tzukanov.narod.ru/convertfs/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%if %{build_diet}
BuildRequires:	dietlibc-devel >= 0.20-1mdk
%endif

%description
ConvertFS is a very simple but extremely powerful toolset which
allows users to convert one file system to another. It works for
converting virtually any filesystem type to virtually any one as
long as they are both block-oriented and supported by Linux for
read/write, and as long as primary filesystem supports sparse
files. 

 * devclone  -  Utility to make clone of the block device (sparse
                file of the same size).
 * devremap  -  Core of the toolset - block relocation utility.
 * prepindex -  Utility to prepare index (list of raw blocks) of
                filesystem image.

%prep

%setup -q -n %{name}
bzcat %{SOURCE1} > README

%build

%if %{build_diet}
    # OE: use the power of dietlibc
    for i in devclone devremap prepindex; do
	diet gcc -s -static -o $i $i.c -Os
    done	
%else
    %make CFLAGS="%{optflags}"
%endif

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}/sbin
install -m755 devclone %{buildroot}/sbin/
install -m755 devremap %{buildroot}/sbin/
install -m755 prepindex %{buildroot}/sbin/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README contrib test convertfs_dumb
/sbin/devclone
/sbin/devremap
/sbin/prepindex
