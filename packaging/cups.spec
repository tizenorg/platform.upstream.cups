Name:           cups
#BuildRequires:  avahi-compat-mDNSResponder-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  libjpeg8-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libopenssl-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig
BuildRequires:  update-desktop-files
BuildRequires:  zlib-devel
# Have libtool as explicit buildrequirement to no longer depend
# on a "hidden" buildrequirement in the OBS project definition:
BuildRequires:  libtool
BuildRequires:  systemd-devel
%{?systemd_requires}
%define have_systemd 1
Requires(pre):         /usr/sbin/groupadd
Url:            http://www.cups.org/
Summary:        The Common UNIX Printing System
License:        GPL-2.0+ ; LGPL-2.1+
Group:          Hardware/Printing
# Source0...Source9 is for sources from upstream:
# URL for Source0: http://ftp.easysw.com/pub/cups/1.5.3/cups-1.5.3-source.tar.bz2
# MD5 sum for Source0 on http://www.cups.org/software.php e1ad15257aa6f162414ea3beae0c5df8
Version:        1.5.3
Release:        0
Source0:        cups-%{version}-source.tar.bz2
# Require the exact matching version-release of the cups-libs sub-package because
# non-matching CUPS libraries may let CUPS software crash (e.g. segfault)
# because all CUPS software is built from the one same CUPS source tar ball
# so that there are CUPS-internal dependencies via CUPS private API calls
# (which do not happen for third-party software which uses only the CUPS public API).
# The exact matching version-release of the cups-libs sub-package is available
# on the same package repository where the cups package is because
# all are built simulaneously from the same cups source package
# and all required packages are provided on the same repository:
Requires:       cups-libs = %{version}-%{release}
Requires:       cups-client = %{version}
# Inherited RPM Requires from the past but I (jsmeix@suse.de) do not know the reason for it:
Requires:       util-linux
Source102:      postscript.ppd.bz2
Source103:      cups.sysconfig
Source105:      PSLEVEL1.PPD.bz2
Source106:      PSLEVEL2.PPD.bz2
Source108:      cups-client.conf
Source109:      baselibs.conf
Source1001: 	cups.manifest
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Requires:       /usr/bin/pdftops
%systemd_requires

%description
The Common UNIX Printing System (CUPS) is the
standards-based, open source printing system.

See http://www.cups.org


%package libs
Summary:        Libraries for CUPS
License:        GPL-2.0+ ; LGPL-2.1+
Group:          Hardware/Printing

%description libs
The Common UNIX Printing System (CUPS) is the
standards-based, open source printing system.

See http://www.cups.org

This package contains libraries needed by CUPS
and other packages.


%package client
Summary:        CUPS Client Programs
License:        GPL-2.0+
Group:          Hardware/Printing
Requires:       cups-libs = %{version}-%{release}

%description client
The Common UNIX Printing System (CUPS) is the
standards-based, open source printing system.

See http://www.cups.org

This package contains all programs needed
for running a CUPS client, not a server.


%package devel
Summary:        Development Environment for CUPS
License:        GPL-2.0+
Group:          Development/Libraries/C and C++
# Do not require the exact matching version-release of cups-libs
# but only a cups-libs package with matching version because
# for building third-party software which uses only the CUPS public API
# there are no CUPS-internal dependencies via CUPS private API calls
# (the latter would require the exact matching cups-libs version-release):
Requires:       cups-libs = %{version}
Requires:       libjpeg-devel
Requires:       libpng-devel
Requires:       libtiff-devel
Requires:       libopenssl-devel
Requires:       pam-devel
Requires:       zlib-devel
Requires:       systemd-devel
Requires:       glibc-devel

%description devel
The Common UNIX Printing System (CUPS) is the
standards-based, open source printing system.

See http://www.cups.org

This is the development package.


%package ddk
Summary:        CUPS Driver Development Kit
License:        GPL-2.0+
Group:          Hardware/Printing
Requires:       cups = %{version}
Requires:       cups-devel = %{version}
# Since CUPS 1.4 the CUPS Driver Development Kit (DDK) is bundled with CUPS.
# For CUPS 1.2.x and 1.3.x, the DDK was separated software
# which we provided (up to openSUSE 11.1 / SLE11) in our cupsddk package:
Provides:       cupsddk = %{version}
Obsoletes:      cupsddk < %{version}

%description ddk
The Common UNIX Printing System (CUPS) is the
standards-based, open source printing system.

See http://www.cups.org

The CUPS Driver Development Kit (DDK) provides
a suite of standard drivers, a PPD file compiler,
and other utilities that can be used to develop
printer drivers for CUPS.


%prep
# Be quiet when unpacking:
%setup -q -n cups-%{version}
cp %{SOURCE1001} .

%build
# Disable SILENT run of make so that make runs verbose as usual:
sed -i -e 's/^\.SILENT:/# .SILENT:/' Makedefs.in
libtoolize --force
aclocal
autoconf
export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS -O2 -fstack-protector"
export CFLAGS="$RPM_OPT_FLAGS -fstack-protector -DLDAP_DEPRECATED"
export CXX=g++
# As long as cups-1.4.3-default-webcontent-path.patch is applied
# configure --with-docdir=... would be no longer needed
# because cups-1.4.3-default-webcontent-path.patch changes the
# default with-docdir path whereto the web content is installed
# from /usr/share/doc/cups to /usr/share/cups/webcontent because the
# files of the CUPS web content are no documentation, see CUPS STR #3578
# and http://bugzilla.novell.com/show_bug.cgi?id=546023#c6 and subsequent comments
# so that the new default could be used as is but upstream may accept
# cups-1.4.3-default-webcontent-path.patch in general but change its default
# so that with-docdir is explicitly set here to be future proof:
./configure \
	--mandir=%{_mandir} \
	--sysconfdir=%{_sysconfdir} \
	--libdir=%{_libdir} \
	--datadir=%{_datadir} \
	--with-docdir=%{_datadir}/cups/webcontent \
	--with-cups-user=lp \
	--with-cups-group=lp \
	--enable-debug \
	--enable-relro \
	--enable-gssapi \
	--disable-static \
	--without-rcdir \
	--enable-dbus \
	--enable-ldap \
	--with-java \
	--with-php \
	--with-python \
	--with-cachedir=/var/cache/cups \
	--with-pdftops=/usr/bin/pdftops \
%if 0%{?have_systemd}
	--with-systemdsystemunitdir=%{_unitdir} \
%endif
	--prefix=/
make %{?_smp_mflags} CXX=g++

%install
make BUILDROOT=$RPM_BUILD_ROOT install
# Use Ghostscript fonts instead of CUPS fonts:
rm -r $RPM_BUILD_ROOT/usr/share/cups/fonts
mkdir -p $RPM_BUILD_ROOT/usr/share/ghostscript/fonts
ln -sf /usr/share/ghostscript/fonts $RPM_BUILD_ROOT/usr/share/cups/
# Make directory for ssl files:
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cups/ssl
# Add a client.conf as template (Source108: cups-client.conf):
install -m644 %{SOURCE108} $RPM_BUILD_ROOT%{_sysconfdir}/cups/client.conf
# Make the libraries accessible also via generic named links:
ln -sf libcupsimage.so.2 $RPM_BUILD_ROOT%{_libdir}/libcupsimage.so
ln -sf libcups.so.2 $RPM_BUILD_ROOT%{_libdir}/libcups.so
# Add missing usual directories:
install -d -m755 $RPM_BUILD_ROOT%{_datadir}/cups/drivers
install -d -m755 $RPM_BUILD_ROOT/var/cache/cups
# Add conf/pam.tizen regarding support for PAM (see Patch100: cups-pam.diff):
install -m 644 -D conf/pam.tizen $RPM_BUILD_ROOT/etc/pam.d/cups
# Add missing usual documentation:
install -d -m755 $RPM_BUILD_ROOT/%{_defaultdocdir}/cups
for f in CHANGES*.txt CREDITS.txt INSTALL.txt LICENSE.txt README.txt
do install -m 644 "$f" $RPM_BUILD_ROOT%{_defaultdocdir}/cups/
done
# Source102: postscript.ppd.bz2
bzip2 -cd < %{SOURCE102} > $RPM_BUILD_ROOT%{_datadir}/cups/model/Postscript.ppd
# Source105: PSLEVEL1.PPD.bz2
bzip2 -cd < %{SOURCE105} > $RPM_BUILD_ROOT%{_datadir}/cups/model/Postscript-level1.ppd
# Source106: PSLEVEL2.PPD.bz2
bzip2 -cd < %{SOURCE106} > $RPM_BUILD_ROOT%{_datadir}/cups/model/Postscript-level2.ppd
find %{buildroot}/usr/share/cups/model -name "*.ppd" | while read FILE
do # Change default paper size from Letter to A4 if possible
   # https://bugzilla.novell.com/show_bug.cgi?id=suse30662
   # and delete trailing whitespace:
   perl -pi -e 's:^(\*Default.*)Letter\s*$:$1A4\n:; \
                s:^(\*ImageableArea A4.*\:\s+)"0 0 595 842":$1"24 48 571 818":; \
                s:^(\*ImageableArea Letter.*\:\s+)"0 0 612 792":$1"24 48 588 768":; \
                s:\s\n:\n:' "$FILE"
   gzip -9 "$FILE"
done
# Add files for desktop menu:
rm -f $RPM_BUILD_ROOT/usr/share/applications/cups.desktop
%tizen_update_desktop_file -i cups PrintingUtility 2>/dev/null
mkdir $RPM_BUILD_ROOT/usr/share/pixmaps
install -m 644 $RPM_BUILD_ROOT/usr/share/icons/hicolor/64x64/apps/cups.png $RPM_BUILD_ROOT/usr/share/pixmaps
rm -rf $RPM_BUILD_ROOT/usr/share/icons
# Remove unpackaged files:
rm -rf $RPM_BUILD_ROOT/%{_mandir}/es/cat?
rm -rf $RPM_BUILD_ROOT/%{_mandir}/fr/cat?
rm -rf $RPM_BUILD_ROOT/%{_mandir}/cat?
# Norwegian is "nb", "zh" is probablyx "zh_CN"
mv $RPM_BUILD_ROOT/usr/share/locale/{no,nb}
mv $RPM_BUILD_ROOT/usr/share/locale/{zh,zh_CN}

rm -rf %{buildroot}/etc/xinetd.d

# Run fdupes:
%fdupes $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -g 71 -o -r ntadmin 2>/dev/null || :

%post
%systemd_post cups.service cups.socket cups.path

%preun
%systemd_preun cups.service cups.socket cups.path

%postun
%systemd_postun cups.service cups.socket cups.path

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%manifest %{name}.manifest
# The files sections list all mandatory files explicitly one by one.
# In particular all executables are listed explicitly.
# This avoids that CUPS' configure magic might silently
# not build and install an executable when whatever condition
# for configure's automated tests is not fulfilled in the build system.
# See https://bugzilla.novell.com/show_bug.cgi?id=526847#c9
# (In CUPS 1.3.10 a configure magic did silently skip to build
#  the pdftops filter when there was no /usr/bin/pdftops
#  installed in the build system regardless of an explicite
#  configure setting '--with-pdftops=/usr/bin/pdftops',
#  see also http://www.cups.org/str.php?L3278).
# When all mandatory files are explicitly listed,
# the build fails intentionally if a mandatory file was not built
# which ensures that already existing correctly built binary RPMs
# are not overwritten by broken RPMs where mandatory files are missing.
%defattr(-,root,root)
%config(noreplace) %attr(640,root,lp) %{_sysconfdir}/cups/cupsd.conf
%{_sysconfdir}/cups/cupsd.conf.default
%config(noreplace) %attr(640,root,lp) %{_sysconfdir}/cups/snmp.conf
%config(noreplace) %attr(755,lp,lp) %{_sysconfdir}/cups/interfaces
%config %{_sysconfdir}/pam.d/cups
%config %{_sysconfdir}/dbus-1/system.d/cups.conf
%dir %attr(700,root,lp) %{_sysconfdir}/cups/ssl
%dir %attr(755,root,lp) %{_sysconfdir}/cups/ppd
%{_bindir}/cupstestppd
%{_sbindir}/cupsaddsmb
%{_sbindir}/cupsctl
%{_sbindir}/cupsd
%{_sbindir}/cupsfilter
%dir /usr/lib/cups
%dir /usr/lib/cups/backend
/usr/lib/cups/backend/http
/usr/lib/cups/backend/https
/usr/lib/cups/backend/ipp
/usr/lib/cups/backend/ipps
/usr/lib/cups/backend/lpd
/usr/lib/cups/backend/parallel
/usr/lib/cups/backend/serial
/usr/lib/cups/backend/snmp
/usr/lib/cups/backend/socket
/usr/lib/cups/backend/usb
%dir /usr/lib/cups/cgi-bin
/usr/lib/cups/cgi-bin/admin.cgi
/usr/lib/cups/cgi-bin/classes.cgi
/usr/lib/cups/cgi-bin/help.cgi
/usr/lib/cups/cgi-bin/jobs.cgi
/usr/lib/cups/cgi-bin/printers.cgi
%dir /usr/lib/cups/daemon
/usr/lib/cups/daemon/cups-deviced
/usr/lib/cups/daemon/cups-driverd
/usr/lib/cups/daemon/cups-exec
/usr/lib/cups/daemon/cups-lpd
/usr/lib/cups/daemon/cups-polld
%dir /usr/lib/cups/driver
%dir /usr/lib/cups/filter
/usr/lib/cups/filter/bannertops
/usr/lib/cups/filter/commandtoescpx
/usr/lib/cups/filter/commandtopclx
/usr/lib/cups/filter/commandtops
/usr/lib/cups/filter/gziptoany
/usr/lib/cups/filter/imagetops
/usr/lib/cups/filter/imagetoraster
/usr/lib/cups/filter/pdftops
/usr/lib/cups/filter/pstops
/usr/lib/cups/filter/rastertodymo
/usr/lib/cups/filter/rastertoepson
/usr/lib/cups/filter/rastertoescpx
/usr/lib/cups/filter/rastertohp
/usr/lib/cups/filter/rastertolabel
/usr/lib/cups/filter/rastertopclx
/usr/lib/cups/filter/rastertopwg
/usr/lib/cups/filter/texttops
%dir /usr/lib/cups/monitor
/usr/lib/cups/monitor/bcp
/usr/lib/cups/monitor/tbcp
%dir /usr/lib/cups/notifier
/usr/lib/cups/notifier/dbus
/usr/lib/cups/notifier/mailto
/usr/lib/cups/notifier/rss
%dir %attr(0775,root,ntadmin) %{_datadir}/cups/drivers
%{_datadir}/applications/cups.desktop
%{_datadir}/pixmaps/cups.png
%doc %{_defaultdocdir}/cups
%doc %{_mandir}/man1/cupstestppd.1.gz
%doc %{_mandir}/man5/classes.conf.5.gz
%doc %{_mandir}/man5/client.conf.5.gz
%doc %{_mandir}/man5/cups-snmp.conf.5.gz
%doc %{_mandir}/man5/cupsd.conf.5.gz
%doc %{_mandir}/man5/mailto.conf.5.gz
%doc %{_mandir}/man5/mime.convs.5.gz
%doc %{_mandir}/man5/mime.types.5.gz
%doc %{_mandir}/man5/printers.conf.5.gz
%doc %{_mandir}/man5/subscriptions.conf.5.gz
%doc %{_mandir}/man7/backend.7.gz
%doc %{_mandir}/man7/filter.7.gz
%doc %{_mandir}/man7/notifier.7.gz
%doc %{_mandir}/man8/cups-deviced.8.gz
%doc %{_mandir}/man8/cups-driverd.8.gz
%doc %{_mandir}/man8/cups-lpd.8.gz
%doc %{_mandir}/man8/cups-polld.8.gz
%doc %{_mandir}/man8/cupsaddsmb.8.gz
%doc %{_mandir}/man8/cupsctl.8.gz
%doc %{_mandir}/man8/cupsd.8.gz
%doc %{_mandir}/man8/cupsfilter.8.gz
%{_datadir}/cups/
%exclude %{_datadir}/cups/ppdc/
%if 0%{?have_systemd}
%{_unitdir}/cups.path
%{_unitdir}/cups.service
%{_unitdir}/cups.socket
%endif

%files client
%manifest %{name}.manifest
# Set explicite owner, group, and permissions for lppasswd
# to enforce to have the upstream owner, group, and permissions in the RPM
# because otherwise our build magic /usr/sbin/Check sets them to lp:lp 2755
# according to /etc/permissions.secure in the build system,
# see https://bugzilla.novell.com/show_bug.cgi?id=574336#c12
# and subsequent comments up to comment #17 therein.
# Even if /etc/permissions.secure in the openSUSE:Factory build system might be
# already fixed, it must also work for build systems for released products.
%defattr(-,root,root)
%{_bindir}/cancel
%{_bindir}/cupstestdsc
%{_bindir}/ipptool
%{_bindir}/lp
%{_bindir}/lpoptions
%attr(0555,root,root) %{_bindir}/lppasswd
%{_bindir}/lpq
%{_bindir}/lpr
%{_bindir}/lprm
%{_bindir}/lpstat
%{_sbindir}/accept
%{_sbindir}/cupsaccept
%{_sbindir}/cupsdisable
%{_sbindir}/cupsenable
%{_sbindir}/cupsreject
%{_sbindir}/lpadmin
%{_sbindir}/lpc
%{_sbindir}/lpinfo
%{_sbindir}/lpmove
%{_sbindir}/reject
%doc %{_mandir}/man1/cancel.1.gz
%doc %{_mandir}/man1/cupstestdsc.1.gz
%doc %{_mandir}/man1/ipptool.1.gz
%doc %{_mandir}/man1/lp.1.gz
%doc %{_mandir}/man1/lpoptions.1.gz
%doc %{_mandir}/man1/lppasswd.1.gz
%doc %{_mandir}/man1/lpq.1.gz
%doc %{_mandir}/man1/lpr.1.gz
%doc %{_mandir}/man1/lprm.1.gz
%doc %{_mandir}/man1/lpstat.1.gz
%doc %{_mandir}/man5/ipptoolfile.5.gz
%doc %{_mandir}/man8/accept.8.gz
%doc %{_mandir}/man8/cupsaccept.8.gz
%doc %{_mandir}/man8/cupsdisable.8.gz
%doc %{_mandir}/man8/cupsenable.8.gz
%doc %{_mandir}/man8/cupsreject.8.gz
%doc %{_mandir}/man8/lpadmin.8.gz
%doc %{_mandir}/man8/lpc.8.gz
%doc %{_mandir}/man8/lpinfo.8.gz
%doc %{_mandir}/man8/lpmove.8.gz
%doc %{_mandir}/man8/reject.8.gz

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/cups/
%{_libdir}/libcups.so
%{_libdir}/libcupsimage.so
%{_libdir}/libcupscgi.so
%{_libdir}/libcupsdriver.so
%{_libdir}/libcupsmime.so
%{_libdir}/libcupsppdc.so
%{_datadir}/cups/ppdc/

%files ddk
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/ppdc
%{_bindir}/ppdhtml
%{_bindir}/ppdi
%{_bindir}/ppdmerge
%{_bindir}/ppdpo
%doc %{_mandir}/man1/ppdc.1.gz
%doc %{_mandir}/man1/ppdhtml.1.gz
%doc %{_mandir}/man1/ppdi.1.gz
%doc %{_mandir}/man1/ppdmerge.1.gz
%doc %{_mandir}/man1/ppdpo.1.gz
%doc %{_mandir}/man5/ppdcfile.5.gz

%files libs
%manifest %{name}.manifest
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/cups/client.conf
%dir %attr(0710,root,lp) %{_var}/spool/cups
%dir %attr(1770,root,lp) %{_var}/spool/cups/tmp
%dir %attr(0755,lp,lp) %{_var}/log/cups/
%dir %attr(0775,lp,lp) %{_var}/cache/cups
%{_bindir}/cups-config
%{_libdir}/libcups.so.*
%{_libdir}/libcupscgi.so.*
%{_libdir}/libcupsdriver.so.*
%{_libdir}/libcupsimage.so.*
%{_libdir}/libcupsmime.so.*
%{_libdir}/libcupsppdc.so.*
%{_datadir}/locale/*/cups_*
%doc %{_mandir}/man1/cups-config.1.gz

%changelog
