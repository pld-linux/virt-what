#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Detect if we are running in a virtual machine
Name:		virt-what
Version:	1.13
Release:	1
License:	GPL v2+
Group:		Applications/Emulators
Source0:	http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz
# Source0-md5:	28d3be1d8981e7fd83c012ebf0d95bb1
Patch0:		bashisms.patch
Patch1:		vserver-type.patch
URL:		http://people.redhat.com/~rjones/virt-what/
# This is provided by the build root, but we make it explicit
# anyway in case this was dropped from the build root in future.
BuildRequires:	/usr/bin/pod2man
%if %{with tests}
# Required at build time in order to do 'make check' (for getopt).
BuildRequires:	util-linux
%endif
# virt-what script uses dmidecode and getopt (from util-linux).
# RPM cannot detect this so make the dependencies explicit here.
%ifarch %{ix86} %{x8664}
Requires:	dmidecode
%endif
Requires:	util-linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
virt-what is a shell script which can be used to detect if the program
is running in a virtual machine.

The program prints out a list of "facts" about the virtual machine,
derived from heuristics. One fact is printed per line.

If nothing is printed and the script exits with code 0 (no error),
then it can mean either that the program is running on bare-metal or
the program is running inside a type of virtual machine which we don't
know about or can't detect.

Current types of virtualization detected:
 - hyperv Microsoft Hyper-V
 - kvm Linux Kernel Virtual Machine (KVM)
 - openvz OpenVZ or Virtuozzo
 - powervm_lx86 IBM PowerVM Lx86 Linux/x86 emulator
 - qemu QEMU (unaccelerated)
 - uml User-Mode Linux (UML)
 - virtage Hitachi Virtualization Manager (HVM) Virtage LPAR
 - virtualbox VirtualBox
 - virtualpc Microsoft VirtualPC
 - vmware VMware
 - xen Xen
 - xen-dom0 Xen dom0 (privileged domain)
 - xen-domU Xen domU (paravirtualized guest domain)
 - xen-hvm Xen guest fully virtualized (HVM)

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%configure
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README COPYING
%attr(755,root,root) %{_sbindir}/virt-what
%attr(755,root,root) %{_libdir}/virt-what-cpuid-helper
%{_mandir}/man1/virt-what.1*
