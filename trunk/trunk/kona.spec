Name:
Version: 
Release: 
Summary: Tool for creating chrooted images from rpms or yum
License: LLNL
Group: System Environment/Kernel
Vendor: LLNL
Source: %{name}-%{version}-%{release}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArchitectures: noarch
Requires: rpm, yum, coreutils, bash
%define __spec_install_post /usr/lib/rpm/brp-compress || :

%description
Tool for creating chrooted images from rpms or yum

%prep
%setup -q -n %{name}-%{version}

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p $RPM_BUILD_ROOT/etc/kona
install -m 555 kona.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/kona
install -m 555 create_rpm_image $RPM_BUILD_ROOT/usr/bin
install -m 555 create_yum_image $RPM_BUILD_ROOT/usr/bin
touch $RPM_BUILD_ROOT/etc/kona/defaults

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%attr(0555,root,root) /usr/bin/create_rpm_image
%attr(0555,root,root) /usr/bin/create_yum_image
%attr(0555,root,root) /etc/sysconfig/kona
%attr(0755,root,root) %dir /etc/kona
%attr(0644,root,root) %config(noreplace) /etc/kona/defaults
