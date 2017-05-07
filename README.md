# Inter-VM Pass password manager for Qubes OS

This is a very simple bridge between Qubes OS VMs.  With it, you can
store and retrieve passwords between VMs without having to grant
any of the VMs any special policy privileges other than access to the
Qubes services implemented here.

## Using the software

These instructions assume you have installed the software.  See the
*Installing the software* heading below for more information.

Run `qvm-pass -?` on a terminal to get usage information.

## Installing the software

There are three components for this software:

* The client `qvm-pass-client` you install in the VMs (or their templates)
  where you want to manage your passwords.
* The service `qvm-pass-service` you install in the VMs (or their templates)
  where you want to store your passwords.
* The policy `qvm-pass-dom0` is the dom0 side of things, necessary to
  enable the services and control access from the clients to the service.

First, build the software,  After cloning this repository on a suitable VM,
run the command:

```
make rpm
```

This will generate three installable packages on the local directory:

* `qvm-pass-client-<version>.noarch.rpm`
* `qvm-pass-service-<version>.noarch.rpm`
* `qvm-pass-dom0-<version>.noarch.rpm`

Copy the `qvm-pass-client-<version>.noarch.rpm` file to the template VM
or standalone VM where you plan to manage passwords.  Install the RPM with
`dnf install <name of the RPM>`.  At this point, this VM, as well as
any VMs using this as a template, have gained the ability to list
and store passwords stored in other VMs.

Now copy the `qvm-pass-service-<version>.noarch.rpm` file to the template
VM or standalone VM where you plan to store passwords.  Install the RPM with
`dnf install <name of the RPM>`.  At this point, this VM, as well as
any VMs using this as a template, have gained the ability to securely store
passwords in `/home/user/.password-store`.

Now copy the `qvm-pass-policy-dom0-<version>.noarch.rpm` file to
your dom0.  At this point, the default policy (`ask`) is active on
your Qubes OS system, and you can begin using the client.

Those clever among you will have discovered that there is a `Makefile`
included, and that you can use the `Makefile` to install the software on
other non-RPM templates.  I welcome pull requests to add support for
other distro packages and Qubes OS templates.

## Troubleshooting and debugging

As always, you can file new issues on the repo of this project for help
with fixing bugs that the programs may have.  Pull requests also welcome.
