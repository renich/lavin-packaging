%global forgeurl https://github.com/cloudamqp/lavinmq
Version:        2.9.2
%forgemeta

Name: lavinmq
Release: %autorelease
Summary: Message queue server that implements the AMQP 0-9-1 protocol
URL: %forgeurl
License: Apache-2.0


# Sources
Source0: %forgesource

# Note: We need two files from this (chart.js and helpers.segment.js)
Source1: https://github.com/chartjs/Chart.js/releases/download/v4.0.1/chart.js-4.0.1.tgz

## additional ones
Source2: https://cdn.jsdelivr.net/npm/chartjs-adapter-luxon@1.3.1/dist/chartjs-adapter-luxon.esm.js

## Note: This one is installed as luxon.js
Source3: https://moment.github.io/luxon/es6/luxon.mjs

## Note: This one is installed as elements-8.2.0.css
Source4: https://unpkg.com/@stoplight/elements@8.2.0/styles.min.css

## Note: This one is installed as elements-8.2.0.js
Source5: https://unpkg.com/@stoplight/elements@8.2.0/web-components.min.js

# Rootless user systemd unit
Source6: lavinmq-user.service


# Prevent Makefile from installing docs (handled by %%doc)
Patch0: 0001-lavinmq-makefile_fixes.patch

# Fix JS imports (applied to Source2)
Patch1: 0002-lavinmq-js-imports.patch


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
mkdir -p static/js/lib/chunks

# Extract and put the files in place
tar -zxOf %{SOURCE1} package/dist/chart.js > static/js/lib/chart.js
tar -zxOf %{SOURCE1} package/dist/chunks/helpers.segment.js > static/js/lib/chunks/helpers.segment.js

cp %{SOURCE2} static/js/lib/chartjs-adapter-luxon.esm.js
patch -p0 static/js/lib/chartjs-adapter-luxon.esm.js < %{PATCH1}

cp %{SOURCE3} static/js/lib/luxon.js
cp %{SOURCE4} static/js/lib/elements-8.2.0.css
cp %{SOURCE5} static/js/lib/elements-8.2.0.js


# TODO: we need to move this one to a networkless procedure
%build
# Ensure Fedora build flags are respected if the upstream Makefile supports them.
# If crystal ignores CFLAGS, that is often acceptable for non-C languages,
# but we still use the macro for parallelism.
%make_build


%install
%make_install UNITDIR=%{_unitdir} SYSUSERSDIR=%{_sysusersdir}

# Install user service unit
install -Dpm 0644 %{SOURCE6} %{buildroot}%{_userunitdir}/%{name}.service

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
