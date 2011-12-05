###############################################################################
###############################################################################
##
##  Copyright (C) 2004-2010 Red Hat, Inc.  All rights reserved.
##
##  This copyrighted material is made available to anyone wishing to use,
##  modify, copy, or redistribute it subject to the terms and conditions
##  of the GNU General Public License v.2.
##
###############################################################################
###############################################################################

# keep around ready for later user
## global alphatag rc4

Name: rgmanager
Summary: Open Source HA Resource Group Failover for Red Hat Cluster
Version: 3.0.12
Release: 10%{?alphatag:.%{alphatag}}%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Base
URL: http://sources.redhat.com/cluster/wiki/
Source0: https://fedorahosted.org/releases/c/l/cluster/%{name}-%{version}.tar.bz2

## patches

Patch1: pass_timeouts_to_resource_agents.patch
Patch2: use_sysrq_b_to_reboot.patch
Patch3: fix_staged_upgrade.patch
Patch4: rgmanager_init_lsb_compliant.patch
Patch5: make_clulog_filter_correctly.patch
Patch6: man_page_improvements.patch

## runtime

Requires: chkconfig initscripts
Requires: cman resource-agents
Requires(post): chkconfig
Requires(preun): initscripts
Requires(preun): chkconfig

## Setup/build bits

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Build dependencies
BuildRequires: clusterlib-devel >= 3.0.0-1
BuildRequires: libxml2-devel ncurses-devel slang-devel

ExclusiveArch: i686 x86_64

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1 -b .pass_timeouts_to_resource_agents
%patch2 -p1 -b .use_sysrq_b_to_reboot
%patch3 -p1 -b .fix_staged_upgrade
%patch4 -p1 -b .rgmanager_init_lsb_compliant
%patch5 -p1 -b .make_clulog_filter_correctly
%patch6 -p1 -b .man_page_improvements

%build
./configure \
  --sbindir=%{_sbindir} \
  --initddir=%{_sysconfdir}/rc.d/init.d \
  --libdir=%{_libdir} \
  --without_fence_agents \
  --without_resource_agents \
  --without_kernel_modules \
  --disable_kernel_check

##CFLAGS="$(echo '%{optflags}')" make %{_smp_mflags}
CFLAGS="$(echo '%{optflags}')" make -C rgmanager all

%install
rm -rf %{buildroot}
make -C rgmanager install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%description
Red Hat Resource Group Manager provides high availability of critical server
applications in the event of planned or unplanned system downtime.

%post
/sbin/chkconfig --add rgmanager

%preun
if [ "$1" = 0 ]; then
	/sbin/service rgmanager stop >/dev/null 2>&1
	/sbin/chkconfig --del rgmanager
fi

%files
%defattr(-,root,root,-)
%doc doc/COPYING.* doc/COPYRIGHT doc/README.licence rgmanager/README rgmanager/errors.txt
%{_sysconfdir}/rc.d/init.d/rgmanager
%{_sbindir}/clu*
%{_sbindir}/rgmanager
%{_sbindir}/rg_test
%{_mandir}/man8/clu*
%{_mandir}/man8/rgmanager*

%changelog
* Mon Jul 12 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-10
- Add failover domain documentation and other improvements
  (man_page_improvements.patch)
  Resolves: rhbz#557563

* Mon Jul 12 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-9
- Make clulog filter correctly based on cluster.conf
  (make_clulog_filter_correctly.patch)
  Resolves: rhbz#609866

* Mon Jul 12 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-8
- Fix patch file naming
  Related: rhbz#612110

* Fri Jul  9 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-7
- Fix rgmanager init script to be more LSB compliant
  (rgmanager_init_lsb_compliant.patch)
  Resolves: rhbz#612110

* Wed Jun 30 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-6
- Fix staged upgrade
  (fix_staged_upgrade.patch)
  Resolves: rhbz#609550

* Wed Jun 30 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-5
- Fix 3.0.12-3 changelog

* Tue Jun 29 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-3
- Use sysrq-b to reboot
  (use_sysrq_b_to_reboot.patch)
  Resolves: rhbz#609181

* Fri Jun 25 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-2
- Pass timeouts to resource agents
  (pass_timeouts_to_resource_agents.patch)
  Resolves: rhbz#606480

* Wed May 12 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-1
- Rebase on top of new upstream bug fix only release:
  * drop all bug fix patches.
  * Addresses the follwing issues from 3.0.12 release:
  Resolves: rhbz#588890, rhbz#588925, rhbz#589131, rhbz#588010
  * Rebase:
  Resolves: rhbz#582350
- Stop build on ppc and ppc64.
  Resolves: rhbz#591000

* Wed Apr  7 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.9-2
- Fix 2+ simultaneous relocation crash
  (fix_2_or_more_simultaneous_relocation_crash.patch)
  Resolves: rhbz#577856
- Fix meory leaks during relocation
  (fix_memory_leaks_during_relocation.patch)
  (fix_memory_leak_during_reconfig.patch)
  Resolves: rhbz#578249

* Tue Mar  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.9-1
- New upstream release
  Resolves: rhbz#569956, rhbz#569953
- spec file update:
  * update spec file copyright date
  * use bz2 tarball

* Thu Feb 25 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-2
- Resolves: rhbz#568011
- Do not build rgmanager on s390 and s390x.

* Tue Jan 12 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-1
- New upstream release

* Mon Dec  7 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.6-1
- New upstream release
- spec file cleanup:
  * use global instead of define
  * use new Source0 url
  * use %name macro more aggressively

* Fri Nov 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.5-1
- New upstream release

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.4-1
- New upstream release

* Tue Sep  1 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.3-1
- Split from cluster srpm
