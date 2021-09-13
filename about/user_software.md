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

[Spack](https://spack.io) is a package manager designed for high performance computing which allows for installation of various versions of softwares required for scientific computing. We provide some commonly used softwares, and you can supplement these by installing your own softwares with spack.

For a full list of the currently installed spack packages run: `spack find`

For more information see [Spack Resources](../getting_started/linux.md#spack)


You can install any of spack's packages by running:

```shell
spack install package_name
```

When spack packages are installed, they are accompanied by a modulefile. Therefore, to use it, you must either run:

```shell
spack load package_name
```

or 

```shell
module load package_name
```

## Additional Software

In general, we recommend users install additional software to their home directory
and independently manage/maintain it. 
