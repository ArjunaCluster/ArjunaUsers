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

## MPI

Arjuna provides MPI support via the [OpenMPI](https://www.open-mpi.org/) module (`module load openmpi/4.1.3`).
Users should load this module if they are using MPI. The following prior installations are deprecated:

- `module load openmpi/4.1.1`
- MPI Installation at `/usr/local/mpirun`

> `/usr/local/mpirun` is on the `PATH` by default. However it is **not supported**, and will be removed in the future.
> Users are __strongly__ encouraged to use `module load openmpi/4.1.3` instead.

### Example MPI Job

```bash
#!/bin/bash
#SBATCH -N 2

module load openmpi/4.1.3
srun hostname
```

### Known Issues

| Issue | Workaround |
|-------|-----------|
| `mpirun` is not found | Use `srun` instead of `mpirun` |
| MPI hangs in an interactive session | This is presently unsupported. We recommend launching jobs from `salloc` instead. |

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
