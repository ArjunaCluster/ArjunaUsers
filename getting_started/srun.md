## `srun`: Submitting Jobs to the Slurm Workload Manager

Slurm is a job scheduling system commly used in High-Performance Computing (HPC) environments to efficiently allocate and manage computing resources among users.
`srun` is a command-line tool used for submitting jobs to the Slurm workload manager, offering a wide range of options for customizing job submission.
With `srun`, users can easily launch jobs that require multiple CPU cores, large amounts of memory, and long runtimes, while taking advantage of the scalability and reliability of the Slurm workload manager.

### `srun` examples

The basic syntax for submitting a job with `srun` is as follows:

```
srun [options] command
```

where `command` is the command or script to be executed. 

To request one node, with 2GB of memory, for 30 minutes, on the `cpu` partition, type:

```
srun --partition=cpu --nodes=1 --mem=2G --time=30 --pty bash
```

Note:
The option `--pty` here is essential.
You cannot enter the srun environment without `--pty`.

You can also get notification by email when the 'srun' environment is ready if you want.
If your email address is AndrewID@andrew.cmu.edu, to request one node, with 1 task, 1GB of memory, for 2 minutes, on the `cpu` partition, type:

```
srun --partition=cpu --ntasks=1 --nodes=1 --mem=1G --time=2 --mail-type=BEGIN --mail-user=AndrewID@andrew.cmu.edu --pty bash
```

You can also submit a job using 'srun'.
To run a Python script named `my_script.py`, using 1 node, 1GB memory, 1 minute, redirecting stdout to 'out', redirect stderr to 'error', on the `debug` partition, type:

```
srun --partition=debug --node=1 --mem=1G --time=1 --output=out --error=error python my_script.py
```

Note: `--out` and `--error` are incompatible with `--pty`.


### Options

`srun` provides a wide range of options for customizing job submission.
Some of the most commonly used are shown above as examples.
You can get further instruction on these options by typing at the Arjuna the following:

```
srun -h
```
