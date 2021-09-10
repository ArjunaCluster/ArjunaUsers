---
layout: default
title: Connecting to Arjuna
parent: Getting Started
nav_order: 2
---

## Connecting to Arjuna

Arjuna is located at `arjuna.psc.edu` to connect, enter the following into a
terminal:

```shell
ssh andrewID@arjuna.psc.edu
```

As Arjuna is on the CMU network, the above command will only work if you are also
connected to the CMU Network (i.e. you are on campus).

When you login to Arjuna, you will be prompted for a password:

1. Enter the password given to you by the Administrator who created your account.
2. Change your password using `passwd`

On subsequent logins, use your newly set password.

### Accessing Arjuna via CMU's VPN

If you are not on campus, you must first connect to [CMU's VPN]. Once connected
you can then `ssh` into Arjuna.

[CMU's VPN]: https://www.cmu.edu/computing/services/endpoint/network-access/vpn/how-to/

## Configuring SSH

The following steps are quality-of-life improvements to default ssh configuration.
They are not required to use Arjuna.

### Private Key Authentication

Instead of authenticating using a password, you can authenticate using
[Private Key Authentication] and skip typing in a password every time.

[Private Key Authentication]: https://help.ubuntu.com/community/SSH/OpenSSH/Keys

First, generate a set of keys to use in authentication. Skip this step if you
already have a public/private key pair (Look for `~/.ssh/id_rsa`);

```shell
ssh-keygen -t rsa
```

You will be prompted for a location to save your keys (The default is fine) and a
passpharse to unlock your keys. Follow the prompts as directed.

> Your private key `~/.ssh/id_rsa` is your password. Treat it as such and do
> not copy it to insecure systems, display it in public space, etc.

Now that you have a key pair, we need to transfer the *public* key to Arjuna.
To do so, run the following command:

```shell
ssh-copy-id andrewID@arjuna.psc.edu
```

You will be prompted for your key's passphrase (if set) and your password for Arjuna.
You can now log in without entering your password!

### Using a SSH Config File

You can simplify logging in to Arjuna by creating an `~/.ssh/config` file to
specify common option (i.e. your username) or create an alias for Arjuna.

For example, the following config will let you connect with `ssh arjuna`
instead of having to type out the full `ssh andrewID@arjuna.psc.edu` each time.

``` conf
Host arjuna
    User andrewID
    HostName arjuna.psc.edu
```

### Sample SSH Configuration File

The following is a sample `~/.ssh/config` that enables some helpful features.

``` conf
# The * wild card means these options apply everywhere
Host *
    # The next three options configure ssh to reuse sockets to the same host.
    # This speeds up your connection time when ssh in from multiple terminals
    # to the same host
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%h-%p    # This is where ssh will save the sockets too
    ControlPersist 600                  # Key connection open for 600 seconds
    AddKeysToAgent yes              # Automatically adds keys to your ssh-agent
    IdentityFile ~/.ssh/id_rsa      # This set your default key for authentication

Host arjuna
    User andrewID
    ForwardAgent yes
    # Forward your SSH agent, so you use your machine's ssh-agent to authenticate
    # to other machines from Arjuna. This way you don't need to manage multiple
    # ssh keypairs to connect to a common service (i.e. GitHub)
    HostName arjuna.psc.edu

# Skip CMU's VPN and connect to Arjuna via unix.andrew.cmu.edu
# You will be prompted for your CMU password to login to unix.andrew.cmu.edu
# before being forwarded to Arjuna
Host arjuna-jump
    User andrewID
    ForwardAgent yes
    ProxyJump andrewID@unix.andrew.cmu.edu
```

For more configuration options see `man ssh_config` or
[ssh_config's documentation](https://man.openbsd.org/ssh_config).



