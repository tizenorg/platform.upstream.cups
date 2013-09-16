#
# "$Id: cups.spec.in 10558 2012-07-27 20:33:27Z mike $"
#
#   RPM "spec" file for CUPS.
#
#   Original version by Jason McMullan <jmcc@ontv.com>.
#
#   Copyright 2007-2012 by Apple Inc.
#   Copyright 1999-2007 by Easy Software Products, all rights reserved.
#
#   These coded instructions, statements, and computer programs are the
#   property of Apple Inc. and are protected by Federal copyright
#   law.  Distribution and use rights are outlined in the file "LICENSE.txt"
#   which should have been included with this file.  If this file is
#   file is missing or damaged, see the license at "http://www.cups.org/".
#

# Conditional build options (--with name/--without name):
#
#   dbus     - Enable/disable DBUS support (default = enable)
#   dnssd    - Enable/disable DNS-SD support (default = enable)
#   static   - Enable/disable static libraries (default = enable)

%{!?_with_dbus: %{!?_without_dbus: %define _with_dbus --with-dbus}}
%{?_with_dbus: %define _dbus --enable-dbus}
%{!?_with_dbus: %define _dbus --disable-dbus}

%{!?_with_dnssd: %{!?_without_dnssd: %define _with_dnssd --with-dnssd}}
%{?_with_dnssd: %define _dnssd --enable-dnssd}
%{!?_with_dnssd: %define _dnssd --disable-dnssd}

%{!?_with_static: %{!?_without_static: %define _without_static --without-static}}
%{?_with_static: %define _static --enable-static}
%{!?_with_static: %define _static --disable-static}

%define _unpackaged_files_terminate_build 0

Summary: CUPS
Name: cups
Version: 1.6.1
Release: 1
License: GPL-2.0+ and LGPL-2.0+
Group: System Environment/Daemons
Source: %{name}-%{version}.tar.gz
Source1001: cups-data.manifest
Source1002: cups-libs.manifest
Source1003: cups.manifest
Source1004: cups.service

Patch01: network-backends-snmp-queries-optional.patch
Patch02: get-ppd-file-for-statically-configured-bonjour-shared-queues.patch
Patch03: usb-backend-reset-after-job-only-for-specific-devices.patch
Patch04: usb-backend-more-quirk-rules.patch
Patch05: printers-c-recognize-remote-cups-queue-via-dnssd-uri.patch
Patch06: avahi-not-considered-at-some-dnssd-conditionals.patch
Patch07: cupsd-conf-remove-obsolete-browse-directives.patch
Patch08: filter-out-all-control-characters-from-the-1284-device-id.patch
Patch09: ipp-backend-did-not-specify-the-compression-used.patch
Patch10: work-around-some-broken-ipp-printers.patch
Patch11: prevent-crash-due-to-null-host-name-or-fqdn-from-avahi.patch
Patch12: fix-crash-on-shutdown-caused-by-broken-avahi-config.patch
Patch13: fix-another-spot-where-avahi-crashes-cupsd-because-it-does-not-handle-null-values-from-its-own-apis.patch
Patch14: ipp-backend-abort-the-outer-loop-if-we-get-a-failure-from-send-document.patch
Patch15: ipp-backend-could-get-stuck-in-an-endless-loop-on-certain-network-errors.patch
Patch16: ipp-backend-did-not-send-cancel-request-to-printers-when-a-job-was-canceled-and-printer-did-not-support-create-job.patch
Patch17: get-ppd-file-for-statically-configured-ipp-shared-queues.patch
Patch18: pidfile.patch
Patch19: ppd-poll-with-client-conf.patch
Patch20: manpage-translations.patch
Patch21: rootbackends-worldreadable.patch
Patch22: airprint-support.patch
Patch23: removecvstag.patch
Patch24: no-conffile-timestamp.patch
Patch25: drop_unnecessary_dependencies.patch
Patch26: reactivate_recommended_driver.patch
Patch27: read-embedded-options-from-incoming-postscript-and-add-to-ipp-attrs.patch
Patch28: do-not-broadcast-with-hostnames.patch
Patch29: cups-deviced-allow-device-ids-with-newline.patch
Patch30: cups-snmp-oids-device-id-hp-ricoh.patch
Patch31: configure-default-browse-protocols.patch
Patch32: add-ipp-backend-of-cups-1.4.patch
Patch33: logfiles_adm_readable.patch
Patch34: default_log_settings.patch
Patch35: confdirperms.patch
Patch36: printer-filtering.patch
Patch37: show-compile-command-lines.patch
Patch38: ppdc-dynamic-linking.patch
Patch39: log-debug-history-nearly-unlimited.patch
Patch40: pstops-based-workflow-only-for-printing-ps-on-a-ps-printer.patch
Patch41: tests-ignore-warnings.patch
Patch42: tests-ignore-usb-crash.patch
Patch43: test-i18n-nonlinux.patch
Patch44: tests-slow-lpstat.patch
Patch45: forward-port-cups-1-5-x-cups-browsing.patch
Patch46: cupsd-no-crash-on-avahi-threaded-poll-shutdown.patch
Patch47: CVE-2012-5519.patch

# Tizen Patch
Patch48: tizen_fix_build_error.patch
Patch49: tizen_fix_temp_path.patch
Patch50: tizen_set_configuration.patch
Patch51: tizen_fix_unable_to_locate_printer.patch
Patch52: tizen_fix_ps_progress.patch
Patch53: tizen_fix_unable_to_find_ipp_printer_temporarily.patch
Patch54: tizen_work_around_samsung_ipp_printer.patch
Patch55: tizen_fix_ignore_sigpipe.patch
Patch56: tizen_add_job_media_progress.patch
Patch57: tizen_fix_cancel_job.patch

# Use buildroot so as not to disturb the version already installed
BuildRoot: /tmp/%{name}-root

# Dependencies...
Requires: %{name}-libs
Requires: avahi-libs
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  libgcrypt-devel
BuildRequires:  avahi-libs
BuildRequires:  avahi-devel
Obsoletes: lpd, lpr, LPRng
Provides: lpd, lpr, LPRng
Obsoletes: cups-da, cups-de, cups-es, cups-et, cups-fi, cups-fr, cups-he
Obsoletes: cups-id, cups-it, cups-ja, cups-ko, cups-nl, cups-no, cups-pl
Obsoletes: cups-pt, cups-ru, cups-sv, cups-zh

%package devel
Summary: CUPS - development environment
Group: Development/Libraries
Requires: %{name}-libs

%package libs
Summary: CUPS - shared libraries
Group: System Environment/Libraries
Provides: libcups1

%package -n cups-data
Summary: CUPS - shared libraries
Group: System Environment/Libraries
Requires: %{name}
Requires: %{name}-libs

%description
CUPS is the standards-based, open source printing system developed by
Apple Inc. for OS X and other UNIX®-like operating systems.

%description devel
This package provides the CUPS headers and development environment.

%description libs
This package provides the CUPS shared libraries.

%description -n cups-data
This package provides CUPS configuration files

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .

%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
#%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
#%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
#%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1

%build
%configure \
    --without-mandir \
    --without-docdir \
    --localedir=/usr/share/cups/locale \
    --sysconfdir=/usr/etc \
    --localstatedir=/opt/var \
    --disable-mallinfo \
    --disable-libpaper \
    --disable-libusb \
    --disable-tcp-wrappers \
    --disable-acl \
    --disable-dbus \
    --without-dbusdir \
    --disable-unit-tests \
    --disable-relro \
    --enable-gssapi \
    --enable-threads \
    --enable-debug \
    --enable-debug-printfs \
    --disable-cdsassl \
    --enable-gnutls \
    --disable-openssl \
    --enable-ssl \
    --enable-avahi \
    --disable-dnssd \
    --disable-pam \
    --enable-largefile \
    --disable-launchd \
    --enable-raw-printing \
    --without-java --without-php --without-python --without-perl --disable-webif \
    --with-languages=en --without-smfmanifestdir \
    --with-local_protocols='dnssd' --without-printcap \
    --with-remote_protocols='dnssd' --with-log-level=debug --with-system-groups=system,root

# If we got this far, all prerequisite libraries must be here.
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make BUILDROOT=$RPM_BUILD_ROOT install

mkdir -p %{buildroot}/usr/share/license
cp %{_builddir}/%{buildsubdir}/LICENSE.txt %{buildroot}/usr/share/license/cups-libs
cp %{_builddir}/%{buildsubdir}/LICENSE.txt %{buildroot}/usr/share/license/cups-data
cp %{_builddir}/%{buildsubdir}/LICENSE.txt %{buildroot}/usr/share/license/cups

mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants
cp %{SOURCE1004} %{buildroot}/usr/lib/systemd/system
ln -s ../cups.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/cups.service

%post
chown -R 5000:5000 /usr/lib/cups/backend/*

%post -n cups-data
mkdir -p /opt/etc/cups/ssl

ln -s /usr/etc/cups/snmp.conf /opt/etc/cups/snmp.conf

if [ -f /usr/lib/rpm-plugins/msm.so ]
then
chsmack -a org.tizen.mobileprint /opt/etc/cups/
chsmack -t /opt/etc/cups/
chsmack -a org.tizen.mobileprint /opt/etc/cups/snmp.conf
fi

chown -R 5000:5000 /opt/etc/cups/
chown -R 5000:5000 /opt/etc/cups/snmp.conf


# Deal with config migration due to CVE-2012-5519 (STR #4223)
IN=/usr/etc/cups/cupsd.conf
OUT=/usr/etc/cups/cups-files.conf
copiedany=no
for keyword in AccessLog CacheDir ConfigFilePerm	\
    DataDir DocumentRoot ErrorLog FatalErrors		\
    FileDevice FontPath Group LogFilePerm		\
    LPDConfigFile PageLog Printcap PrintcapFormat	\
    RemoteRoot RequestRoot ServerBin ServerCertificate	\
    ServerKey ServerRoot SMBConfigFile StateDir		\
    SystemGroup SystemGroupAuthKey TempDir User; do
    if ! /bin/grep -iq ^$keyword "$IN"; then continue; fi
    copy=yes
    if /bin/grep -iq ^$keyword "$OUT"; then
	if [ "`/bin/grep -i ^$keyword "$IN"`" ==	\
	     "`/bin/grep -i ^$keyword "$OUT"`" ]; then
	    copy=no
	else
	    /bin/sed -i -e "s,^$keyword,#$keyword,i" "$OUT" || :
	fi
    fi
    if [ "$copy" == "yes" ]; then
	if [ "$copiedany" == "no" ]; then
	    (cat >> "$OUT" <<EOF

# Settings automatically moved from cupsd.conf by RPM package:
EOF
	    ) || :
	fi

	(/bin/grep -i ^$keyword "$IN" >> "$OUT") || :
	copiedany=yes
    fi

    /bin/sed -i -e "s,^$keyword,#$keyword,i" "$IN" || :
done
exit 0

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files
%manifest cups.manifest
/usr/share/license/%{name}
/usr/bin/ppdc
/usr/bin/cancel
/usr/bin/cupstestdsc
/usr/bin/cupstestppd
/usr/bin/ipptool
/usr/bin/lp
/usr/bin/lpoptions
/usr/bin/lppasswd
/usr/bin/lpstat
%attr(0755,root,root) %dir /usr/lib/cups
%attr(0755,root,root) %dir /usr/lib/cups/backend
/usr/lib/cups/backend/dnssd
/usr/lib/cups/backend/http
/usr/lib/cups/backend/https
/usr/lib/cups/backend/ipp
#/usr/lib/cups/backend/ipp14
/usr/lib/cups/backend/ipps
/usr/lib/cups/backend/lpd
/usr/lib/cups/backend/snmp
/usr/lib/cups/backend/socket
/usr/lib/cups/backend/usb
%exclude %attr(0755,root,root) %dir /usr/lib/cups/cgi-bin
%exclude /usr/lib/cups/cgi-bin/*
%attr(0755,root,root) %dir /usr/lib/cups/daemon
/usr/lib/cups/daemon/cups-deviced
/usr/lib/cups/daemon/cups-driverd
/usr/lib/cups/daemon/cups-exec
/usr/lib/cups/daemon/cups-polld
%dir /usr/lib/cups/driver
%attr(0755,root,root) %dir /usr/lib/cups/filter
/usr/lib/cups/filter/*
%exclude /usr/lib/cups/filter/rastertodymo
%exclude /usr/lib/cups/filter/rastertoepson
%exclude /usr/lib/cups/filter/rastertohp
%exclude /usr/lib/cups/filter/rastertolabel
%attr(0755,root,root) %dir /usr/lib/cups/monitor
/usr/lib/cups/monitor/*
%attr(0755,root,root) %dir /usr/lib/cups/notifier
%exclude /usr/lib/cups/notifier/*
%attr(0755, root, root) /usr/sbin/cupsaccept
%attr(0755, root, root) /usr/sbin/cupsaddsmb
%attr(0755, root, root) /usr/sbin/cupsctl
%attr(0755, root, root) /usr/sbin/cupsd
%attr(0755, root, root) /usr/sbin/cupsfilter
%attr(0755, root, root) /usr/sbin/lpadmin
%attr(0755, root, root) /usr/sbin/lpc
%attr(0755, root, root) /usr/sbin/lpinfo
%attr(0755, root, root) /usr/sbin/lpmove
%attr(-,root,root) %dir /usr/share/cups
%dir /usr/share/cups/mime
/usr/share/cups/mime/*
%dir /usr/share/cups/model
%dir /usr/share/cups/ppdc
/usr/share/cups/ppdc/*

%files libs
%manifest cups-libs.manifest
/usr/share/license/cups-libs
/usr/lib/*.so.*

%files devel
%{_bindir}/cups-config
%{_libdir}/*.so
%{_includedir}/cups
/usr/share/cups/ipptool/*
/usr/lib/cups/backend/pseudo

%files -n cups-data
%manifest cups-data.manifest
/usr/share/license/cups-data
/usr/etc/cups/*.conf
%dir /usr/etc/cups/interfaces
/usr/lib/systemd/system/cups.service
/usr/lib/systemd/system/multi-user.target.wants/cups.service

