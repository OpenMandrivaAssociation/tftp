Summary: 	The client and server for the Trivial File Transfer Protocol (TFTP)
Name: 		tftp
Version: 	5.2
Release: 	1
License: 	BSD
Group: 		System/Servers
URL:		http://www.kernel.org/pub/software/network/tftp/tftp-hpa
Source0: 	http://www.kernel.org/pub/software/network/tftp/tftp-hpa/tftp-hpa-%{version}.tar.xz
Source1:	https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp.socket
# NOTE: This is ***NOT*** Fedora's service file.
# It has been updated to follow filesystem standards
# and serve stuff from /srv/tftp rather than /var/lib/tftpboot.
Source2:	tftp.service
Patch1:		https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-0.40-remap.patch
Patch2:		https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-hpa-0.39-tzfix.patch
Patch3:		https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-0.42-tftpboot.patch
Patch4:		https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-0.49-chk_retcodes.patch
Patch5:		https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-hpa-0.49-fortify-strcpy-crash.patch
Patch6:		https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-0.49-cmd_arg.patch
Patch7:		https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-hpa-0.49-stats.patch
Patch8:		https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-hpa-5.2-pktinfo.patch
Patch9:		https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-doc.patch
Patch10:	https://src.fedoraproject.org/rpms/tftp/raw/master/f/tftp-enhanced-logging.patch
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

%description	server
The Trivial File Transfer Protocol (TFTP) is normally used only for booting
diskless workstations.  The tftp-server package provides the server for TFTP,
which allows users to transfer files to and from a remote machine. TFTP
provides very little security, and should not be enabled unless it is
expressly needed. The TFTP server is run from %{_sysconfdir}/xinetd.d/tftp,
and is disabled by default on a Mandriva Linux systems.

%prep
%setup -q  -n tftp-hpa-%{version}
%apply_patches
./autogen.sh
autoheader

%build
%serverbuild
%configure

# Doesn't like parallel builds...
make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_unitdir}

make INSTALLROOT=%{buildroot} SBINDIR=%{_sbindir} MANDIR=%{_mandir} install
install -m755 -d %{buildroot}%{_localstatedir}/lib/tftpboot/
install -m644 %{S:1} -D %{buildroot}%{_unitdir}/
install -m644 %{S:2} -D %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}/srv/tftp

%files
%defattr(-,root,root)
%{_bindir}/tftp
%{_mandir}/man1/*

%files server
%defattr(-,root,root)
%dir /srv/tftp
%{_sbindir}/in.tftpd
%{_mandir}/man8/*
%{_unitdir}/tftp.*
