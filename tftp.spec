Summary: 	The client and server for the Trivial File Transfer Protocol (TFTP)
Name: 		tftp
Version: 	5.1
Release: 	4
License: 	BSD
Group: 		System/Servers
URL:		http://www.kernel.org/pub/software/network/tftp/
Source0: 	http://www.kernel.org/pub/software/network/tftp/tftp-hpa/tftp-hpa-%{version}.tar.xz
Source1: 	tftp-xinetd
Patch0:		tftp-mips.patch
Patch1:		tftp-0.40-remap.patch
Patch2:		tftp-hpa-0.39-tzfix.patch
Patch3:		tftp-0.42-tftpboot.patch
Patch4:		tftp-0.49-chk_retcodes.patch
Patch5:		tftp-hpa-0.49-fortify-strcpy-crash.patch
Patch6:		tftp-0.49-cmd_arg.patch
Patch7:		tftp-hpa-0.49-stats.patch
BuildRequires:	tcp_wrappers-devel readline-devel

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for booting
diskless workstations. The tftp package provides the user interface for TFTP,
which allows users to transfer files to and from a remote machine. This
program, and TFTP, provide very little security, and should not be enabled
unless it is expressly needed.

%package	server
Summary:	The server for the Trivial File Transfer Protocol (TFTP)
Group:		System/Servers
Requires:	xinetd
Requires(post):	rpm-helper
Requires(preun):rpm-helper

%description	server
The Trivial File Transfer Protocol (TFTP) is normally used only for booting
diskless workstations.  The tftp-server package provides the server for TFTP,
which allows users to transfer files to and from a remote machine. TFTP
provides very little security, and should not be enabled unless it is
expressly needed. The TFTP server is run from %{_sysconfdir}/xinetd.d/tftp,
and is disabled by default on a Mandriva Linux systems.

%prep
%setup -q  -n tftp-hpa-%{version}
%patch0 -p1
%patch1 -p1 -b .zero~
%patch2 -p1 -b .tzfix~
%patch3 -p1 -b .tftpboot~
%patch4 -p1 -b .chk_retcodes~
%patch5 -p1 -b .fortify-strcpy-crash~
%patch6 -p1 -b .cmd_arg~
%patch7 -p1 -b .stats~
autoreconf

%build
%serverbuild

%configure2_5x

%make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
mkdir -p %{buildroot}%{_sbindir}

make INSTALLROOT=%{buildroot} MANDIR=%{_mandir} install
install -m755 -d %{buildroot}%{_localstatedir}/lib/tftpboot/
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/xinetd.d/tftp

%post server
%_post_service %{name}

%preun server
%_preun_service %{name}

%files
%defattr(-,root,root)
%{_bindir}/tftp
%{_mandir}/man1/*

%files server
%defattr(-,root,root)
%dir %{_localstatedir}/lib/tftpboot
%config(noreplace) %{_sysconfdir}/xinetd.d/tftp
%{_sbindir}/in.tftpd
%{_mandir}/man8/*


%changelog
* Sat Nov 26 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.1-1
+ Revision: 733628
- sync with fedora patches
- enable tcp_wrappers & readline support
- remove old junk
- new version

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 5.0-6
+ Revision: 670679
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 5.0-5mdv2011.0
+ Revision: 607993
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 5.0-4mdv2010.1
+ Revision: 520282
- rebuilt for 2010.1

* Mon Sep 28 2009 Olivier Blin <blino@mandriva.org> 5.0-3mdv2010.0
+ Revision: 450387
- fix __progname usage for mips build (from Arnaud Patard)

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 5.0-2mdv2010.0
+ Revision: 427349
- rebuild

* Sun Mar 22 2009 Oden Eriksson <oeriksson@mandriva.com> 5.0-1mdv2009.1
+ Revision: 360449
- 5.0

* Thu Jan 15 2009 Jérôme Soyer <saispo@mandriva.org> 0.49-1mdv2009.1
+ Revision: 329770
- New upstream release

* Mon Aug 18 2008 Erwan Velu <erwan@mandriva.org> 0.48-1mdv2009.0
+ Revision: 273321
- 0.48

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.42-5mdv2009.0
+ Revision: 225690
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.42-4mdv2008.1
+ Revision: 179647
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.42-3mdv2007.1
+ Revision: 145574
- Import tftp

* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.42-3mdv2007.1
- use the %%mrel macro

* Fri Apr 28 2006 Nicolas L�cureuil <neoclust@mandriva.org> 0.42-2mdk
- s/Mandrakelinux/Mandriva Linux/

* Fri Apr 21 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.42-1mdk
- New release 0.42
- fix prereq

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.40-3mdk
- Rebuild

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.40-2mdk
- rebuild for new readline
- fix summary-ended-with-dot

* Thu Dec 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.40-1mdk
- 0.40
- drop malta patch (P0)

* Wed May 05 2004 Juan Quintela <quintela@mandrakesoft.com> 0.36-1mdk
- 0.36.

* Tue Apr 06 2004 Michael Scherer <misc@mandrake.org> 0.34-2mdk
- removed forbidden word

