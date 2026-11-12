%global forgeurl https://github.com/cloudamqp/lavinmq
Version:        2.11.0
%forgemeta

Name: lavinmq
Release: %autorelease
Summary: Message queue server that implements the AMQP 0-9-1 protocol
URL: %forgeurl
License: Apache-2.0


# Sources
Source0: %forgesource

# Note: We need two files from this (uPlot.esm.js and uPlot.min.css)
Source1: https://registry.npmjs.org/uplot/-/uplot-1.6.32.tgz

## Note: This one is installed as elements-8.2.0.css
Source2: https://unpkg.com/@stoplight/elements@8.2.0/styles.min.css

## Note: This one is installed as elements-8.2.0.js
Source3: https://unpkg.com/@stoplight/elements@8.2.0/web-components.min.js

# Rootless user systemd unit
Source4: lavinmq-user.service


# Prevent Makefile from installing docs (handled by %%doc)
Patch0: 0001-lavinmq-makefile_fixes.patch


# Required for forge macros
BuildRequires: forge-srpm-macros

# systemd (sysusers and user units)
BuildRequires: systemd-rpm-macros

# Building
BuildRequires: gcc
BuildRequires: make

# External
BuildRequires: crystal
BuildRequires: shards

# Other
BuildRequires: lz4-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel

# Documentation
BuildRequires: help2man

# Testing
%if 0%{?fedora} && 0%{?fedora} < 45
BuildRequires: etcd
%endif
%description
A resource efficient message queue server implementing the AMQP protocol.


%prep
%forgeautosetup -N

# Apply the Makefile patch
%patch -p 1 -P 0

# Create target directories
mkdir -p static/js/lib

# Extract and put the files in place
tar -zxOf %{SOURCE1} package/dist/uPlot.esm.js > static/js/lib/uplot.esm.js
tar -zxOf %{SOURCE1} package/dist/uPlot.min.css > static/js/lib/uplot.css

cp %{SOURCE2} static/js/lib/elements-8.2.0.css
cp %{SOURCE3} static/js/lib/elements-8.2.0.js


# TODO: we need to move this one to a networkless procedure
%build
export CRYSTAL_CACHE_DIR="%{_builddir}/.crystal-cache"

# Ensure Fedora build flags are respected if the upstream Makefile supports them.
# If crystal ignores CFLAGS, that is often acceptable for non-C languages,
# but we still use the macro for parallelism.
%make_build


%install
%make_install UNITDIR=%{_unitdir} SYSUSERSDIR=%{_sysusersdir}

# Install user service unit
install -Dpm 0644 %{SOURCE4} %{buildroot}%{_userunitdir}/%{name}.service

# Create the data directory
install -d -m 0750 %{buildroot}%{_sharedstatedir}/%{name}


%check
# Unset NOTIFY_SOCKET so reload tests inside container environments don't attempt
# to send datagrams to the host's protected /run/host/notify socket.
unset NOTIFY_SOCKET || true

# Clustering and port-binding tests require running daemons / fixed ports
# that are not reliably available in isolated container buildroots.
rm -f spec/clustering_spec.cr spec/launcher_bind_spec.cr

# Run tests if possible. Adjust based on actual test command.
%if 0%{?fedora} && 0%{?fedora} < 45
make test
%endif


%post
%systemd_post %{name}.service
%systemd_user_post %{name}.service


%preun
%systemd_preun %{name}.service
%systemd_user_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service
%systemd_user_postun_with_restart %{name}.service


%files
%license LICENSE
%doc README.md NOTICE CHANGELOG.md
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%dir %attr(0750, %{name}, %{name}) %{_sharedstatedir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}ctl
%{_bindir}/%{name}perf
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}ctl.1*
%{_mandir}/man1/%{name}perf.1*
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_userunitdir}/%{name}.service


%changelog
%autochangelog
