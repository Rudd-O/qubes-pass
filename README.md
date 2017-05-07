# Inter-VM Pass password manager for Qubes OS

This is a very simple password management system that lets you
securely store passwords in a compartment fully isolated from
your other compartments.

It accomplishes this feat by by leveraging both
the excellent [`pass`](https://passwordstore.org/) program, and
Qubes OS IPC to isolate the actual password store — and the
master password for the store — from the environments where you
may use the passwords in the store.

With this program, you can store and retrieve passwords between VMs
without having to grant any of the VMs any special policy privileges
other than access to the Qubes services implemented here.

## Using the software

These instructions assume you have installed the software.  See the
*Installing the software* heading below for more information.

Step 1: decide which VM you'll use to manage passwords, and which
VM you'll use to store passwords in.

In the password manager VM, create the file `/rw/config/pass-split-domain`
and add the name of the password store VM as the first and only
line of the file.

Now, from the password manager VM, run the command:

```
qvm-pass init
```

This step will create the necessary GPG keys and password store database
in the password store VM.  You'll receive a Qubes policy prompt asking
you whether to allow your password manager VM to access `ruddo.PassManage`
— it is safe to say yes.  You will then receive a password prompt from
GPG, confirming the creation of the key and the password that, in the
future, will be used to encrypt and access the password store.

Note: don't forget to back your password store VM up regularly!

At this point, you are ready to `list`, `insert` and run other operations
in your password store VM.  `list` and `get` operations will use the
service `ruddo.PassRead`, while management operations will use the
service `ruddo.PassManage`, which allows you to set different policies
for different VMs based on what you want these VMs to be able to do with
the password store VM.

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
