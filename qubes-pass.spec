%define debug_package %{nil}

%define mybuildnumber %{?build_number}%{?!build_number:1}

Name:           qubes-pass
Version:        0.1.0
Release:        %{mybuildnumber}%{?dist}
Summary:        Inter-VM pass password management for Qubes OS AppVMs and StandaloneVMs
BuildArch:      noarch

License:        GPLv3+
URL:            https://github.com/Rudd-O/%{name}
Source0:        https://github.com/Rudd-O/%{name}/archive/{%version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  make
Requires:       python3
Requires:       qubes-core-agent-qrexec

%package service
Summary:        Service package for Qubes OS dom0s that services %{name}

Requires:       pass
Requires:       /bin/egrep
Requires:       coreutils
Requires:       util-linux

%package dom0
Summary:        Policy package for Qubes OS dom0s that arbitrates %{name}
Requires:       qubes-core-dom0 >= 4.1

%description
This package lets you setup a safe password management VM and then
manage the password store remotely from other VMs.  You are meant to
install this package on the VM or template where you want to access
and manage your password store.

%description service
This package lets you serve a safe password store to other VMs.
You are meant to install this package on the VM or template where
you want to keep your password store safe.

%description dom0
This package contains the Qubes OS execution policy for the %{name} package.
You are meant to install this package on the dom0 of the machine where you
have VMs that have the %{name} package installed.

%prep
%setup -q

%build
# variables must be kept in sync with install
make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} SYSCONFDIR=%{_sysconfdir} LIBEXECDIR=%{_libexecdir}

%install
rm -rf $RPM_BUILD_ROOT
# variables must be kept in sync with build
for target in install-client install-service install-dom0; do
    make $target DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} SYSCONFDIR=%{_sysconfdir} LIBEXECDIR=%{_libexecdir}
done

%check
if grep -r '@.*@' --exclude='*.policy' $RPM_BUILD_ROOT ; then
    echo "Check failed: files with AT identifiers appeared" >&2
    exit 1
fi

%files
%attr(0755, root, root) %{_bindir}/qvm-pass
%attr(-, -, -) %{_libexecdir}/%{name}/pass
%doc README.md

%files service
%attr(0755, root, root) %{_sysconfdir}/qubes-rpc/ruddo.PassRead
%attr(0755, root, root) %{_sysconfdir}/qubes-rpc/ruddo.PassManage

%files dom0
%config(noreplace) %attr(0664, root, qubes) %{_sysconfdir}/qubes/policy.d/90-qubes-pass.policy

%changelog
* Mon Jan 31 2022 Manuel Amador (Rudd-O) <rudd-o@rudd-o.com>
- Correct issues with argument parsing again.
