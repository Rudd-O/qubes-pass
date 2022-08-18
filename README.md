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

### Details and features

1. The actual password store is stored in a separate VM, decrypted solely on demand from it, and sent to the VM you manage / request the from.
2. You do not need to set up your own GPG key, as `qvm-pass init` does it for you.
3. There are two different services  one for read-only access and one for read-write.
4. There is a `get-or-generate` feature, not available in normal `pass`, which is useful for stuff like programs that need a password generated and then remembered (such as the excellent [`qubes-pass` Ansible lookup plugin](https://github.com/Rudd-O/ansible-qubes/tree/master/lookup_plugins).
5. The program `mlockall()`s during execution, which prevents passwords from being swapped to the disk of the VM running `qvm-pass`.  Dishonorable exceptions from this security feature are the `-c` and `-q` command-line options, since these run `bash` scripts to do their work, and `bash` cannot lock memory.

*Tip:* combine this program with the excellent [`qubes-pass` lookup plugin
for Ansible Qubes](https://github.com/Rudd-O/ansible-qubes) or the
[`pass` lookup plugin for Ansible](https://github.com/gcoop-libre/ansible-lookup-plugin-pass)
so that you can securely manage VMs and machines that require secrets.

### Compatibility

This program is supported only in Qubes 4.1, although it may work in
earlier versions.

## Using the software

These instructions assume you have installed the software.  See the
*Installing the software* heading below for more information.

Step 1: decide which VM you'll use to manage passwords, and which
VM you'll use to store passwords in.

In the password store VM, make sure that the GPG key you'll use to
encrypt the pass store is available there.  Make a note of the GPG
ID of that key.

In the password manager VM, create the file `/rw/config/pass-split-domain`
and add the name of the password store VM as the first and only
line of the file.

Now, from the password manager VM, run the command:

```
qvm-pass init <GPG key ID available in the password store VM>
```

This step will initialize the password store database in the password store
VM.  You'll receive a Qubes policy prompt asking you whether to allow your
password manager VM to access `ruddo.PassManage` — it is safe to say yes.
You will then receive a confirmation that the pass store has been created
and is encrypting keys with the specified GPG key ID.

Note: don't forget to back your password store VM up regularly!
Both your GPG ID and your encrypted passwords are there.

At this point, you are ready to list, `insert` and run other operations
in your password store VM.  list and get operations will use the
service `ruddo.PassRead`, while management operations will use the
service `ruddo.PassManage`, which allows you to set different policies
for different VMs based on what you want these VMs to be able to do with
the password store VM.

Run `qvm-pass -?` on a terminal to get usage information.

*Tip:* fool programs that use `pass` into using `qvm-pass` instead.
After installation, you can `export PATH=/usr/libexec/qubes-pass:$PATH`
prior to invoking said programs, to induce programs (which invoke the
pass store command line program) to invoke `qvm-pass` instead.

## Installing the software

There are three components for this software:

* The client `qubes-pass` you install in the VMs (or their templates)
  where you want to manage your passwords.
* The service `qubes-pass-service` you install in the VMs (or their templates)
  where you want to store your passwords.
* The policy `qubes-pass-dom0` is the dom0 side of things, necessary to
  enable the services and control access from the clients to the service.

Here's how you install `qubes-pass` on Fedora VMs (*see below for other OSes*):

After cloning this repository on a suitable VM, and installing the
`rpm-build` package onto that VM, run the command:

```
make rpm
```

This will generate three installable packages on the local directory:

* `qubes-pass-<version>.noarch.rpm`
* `qubes-pass-service-<version>.noarch.rpm`
* `qubes-pass-dom0-<version>.noarch.rpm`

Copy the `qubes-pass-<version>.noarch.rpm` file to the template VM
or standalone VM where you plan to manage passwords.  Install the RPM with
`dnf install <name of the RPM>`.  At this point, this VM, as well as
any VMs using this as a template, have gained the ability to list
and store passwords stored in other VMs.

Now copy the `qubes-pass-service-<version>.noarch.rpm` file to the template
VM or standalone VM where you plan to store passwords.  Install the RPM with
`dnf install <name of the RPM>`.  At this point, this VM, as well as
any VMs using this as a template, have gained the ability to securely store
passwords in `/home/user/.password-store`.

Now power off any template VMs you've installed software into,
as well as any VMs based on that template VM you plan to use the
software from.

Now copy the `qubes-pass-dom0-<version>.noarch.rpm` file to your dom0.
At this point, the default policy (which is `ask`) is active on
your Qubes OS system, and you can begin using the client.

Those clever among you will have discovered that there is a `Makefile`
included, and that you can use the `Makefile` to install the software
on other non-RPM, non-Fedora templates.  I welcome pull requests to add
support for other distro packages and Qubes OS templates.  Thanks in
advance for your help.

## Troubleshooting and debugging

As always, you can file new issues on the repo of this project for help
with fixing bugs that the programs may have.  Pull requests also welcome.
