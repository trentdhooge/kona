Name: kona
Version: 1
Release: 15%{?dist}
Summary: Tool for creating chrooted images from rpms or yum
License: GPL
Group: System Environment/Kernel
Vendor: LLNL
Source: %{name}-%{version}-%{release}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArchitectures: noarch
Requires: rpm, yum, coreutils, bash, qemu-img

%if 0%{rhel} > 6
Requires: grub2
%else
Requires: grub
%endif

%define __spec_install_post /usr/lib/rpm/brp-compress || :

%description
Tool for creating chrooted images from rpms or yum

%prep
%setup -q -n %{name}-%{version}-%{release}

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p $RPM_BUILD_ROOT/etc/kona
mkdir -p $RPM_BUILD_ROOT/usr/share/kona
install -m 555 kona.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/kona
install -m 555 create_rpm_image $RPM_BUILD_ROOT/usr/bin
install -m 555 create_yum_image $RPM_BUILD_ROOT/usr/bin
cp qemu/* $RPM_BUILD_ROOT/usr/share/kona
touch $RPM_BUILD_ROOT/etc/kona/defaults
cp GPL.txt $RPM_BUILD_ROOT/usr/share/kona

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%attr(0555,root,root) /usr/bin/create_rpm_image
%attr(0555,root,root) /usr/bin/create_yum_image
%attr(0555,root,root) /etc/sysconfig/kona
%attr(0755,root,root) %dir /etc/kona
%attr(0644,root,root) %config(noreplace) /etc/kona/defaults
%attr(0755,root,root) %dir /usr/share/kona
%attr(0644,root,root) %config /usr/share/kona/passwd
%attr(0644,root,root) %config /usr/share/kona/group
%attr(0400,root,root) %config /usr/share/kona/shadow
%attr(0644,root,root) %config /usr/share/kona/network
%attr(0644,root,root) %config /usr/share/kona/ifcfg-eth0
%attr(0644,root,root) /usr/share/kona/grub.conf
%attr(0444,root,root) /usr/share/kona/fstab
%attr(0444,root,root) /usr/share/kona/GPL.txt

%changelog
* Mon May 18 2015 Trent D'Hooge <tdhooge@llnl.gov>
  - added nbd support from silva50@llnl.gov

* Thu Nov 20 2014 Trent D'Hooge <tdhooge@llnl.gov>
  - Require grub2 on > RHEL6

* Tue Apr 16 2013 Trent D'Hooge <tdhooge@llnl.gov>
  - Define PATH in create_*_image

  - set $releasever in create_yum_image for repos that use that variable
    https://lc.llnl.gov/jira/browse/TOSS-2025
    
  - run lsof on chrooted image and kill anything running in it
    https://lc.llnl.gov/jira/browse/TOSS-2024

* Fri Jul 27 2012 Trent D'Hooge <tdhooge@llnl.gov>
  - attempt to use grubby to update grub.conf file
    so new RH kernel will properly update grub.conf
    if a new kernel is installed into the image
  - add network and ifcfg-eth0 files so network can start
    defaults to dhcp, no name defined
