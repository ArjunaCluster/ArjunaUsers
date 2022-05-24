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

## Additional Software

If you need additional software on Arjuna, we recommend installing it via spack. Many commonly used scientific and engineering packages are provided via the system-wide spack installation. For a full list of the currently installed spack packages run: `spack find`

If a spack package is not available for the software you need, install it from source or binaries.


## Spack

[Spack](https://spack.io) is a package manager designed for high performance computing which allows for installation of various versions of softwares required for scientific computing. We provide some commonly used softwares, and you can supplement these by installing your own softwares with spack.

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


## MPI
> This section will discuss usage of MPI on Arjuna, and presumes familiarity with MPI.

Arjuna provides MPI support via the [OpenMPI](https://www.open-mpi.org/) version 4.1.3 module (`module load openmpi`).
Users should load this module if they are using MPI. The following prior installations are deprecated and not recomended:

- `module load openmpi/4.1.1`
- MPI Installation at `/usr/local/mpirun`

> `/usr/local/mpirun` is on the `PATH` by default. However it is **not supported**, and will be removed in the future.
> Users are __strongly__ encouraged to use `module load openmpi` instead.

Using legacy launchers (i.e. `mpirun` or `mpiexec`) is __not supported__ using the provided `openmpi` and __not recommended__ on other mpi installations. Please use `srun` to launch mpi jobs. 

If users need a different version of MPI than the ones provided, they can install their own via spack or other build tools. Users are advised to first read the [slurm documentation regarding mpi](https://slurm.schedmd.com/mpi_guide.html) before installing MPI, and make sure to build MPI with PMI and slurm support.

### PMI
Arjuna has support for `pmi`, `pmi2`, and `pmix`. To run a job using a specified pmi, launch your jobs using the `--mpi` flag provided by `srun`. If you are unsure of what to use, we recommend trying `--mpi=pmix` first.

### Interactive MPI Jobs
Running MPI Jobs from within interactive jobs launched via `srun <options> --pty bash` is __not supported__ (and will hang). 


### Example MPI Job


```bash
#!/bin/bash
#SBATCH -N <N>
#SBATCH -n <n>
#SBATCH -A <account>
#SBATCH -p <partition>

module load openmpi/4.1.3
srun --mpi=pmix <executable>
```

