---
title: User Software
layout: default
parent: About Arjuna
nav_order: 2
---

# Software

Arjuna uses `modules` to provide access to some common software packages and tools.
For a complete list of the currently available software run: `module avail`

To load a module named `module_name` run: `module load module_name`

For more information, see [Lmod's documentation](https://lmod.readthedocs.io).


## Spack

[Spack](https://spack.io) is a package manager for supercomputers that makes
installing scientific software easy, and tuning installs for a particular
machine. Arjuna uses spack to install and manage the software provided
via modules.

You can install any of spack's 5843 (and counting) packages by running:

```shell
spack install package_name
```

In addition to the common tools provided via modules, we provide their dependencies
as an [upstream spack installation](https://spack.readthedocs.io/en/latest/chain.html?highlight=upstream#using-multiple-upstream-spack-instances). This allows you to
reuses those tools when installing additional software via spack.

For a full list of the currently installed spack packages run: `spack find`

For more information see [Spack Resources](../getting_started/linux.md#spack)

## Additional Software

In general, we recommend users install additional software to their home directory
and independently manage/maintain it. As files placed in a user's home directory
are immediately available on the compute nodes via the [RAID storage].

[RAID storage]: hardware.md#storage
