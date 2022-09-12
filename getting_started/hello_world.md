---
title: Your First Job
layout: default
parent: Getting Started
nav_order: 3
---

# Submitting Your First Job

This tutorial will guide you through the process of submitting your first job on
Arjuna. This tutorial assumes you've already done the following items

1. Login to Arjuna via `ssh`
2. Some familiarity with entering commands at a `bash` shell
3. Some familiarity with `vim` or another command-line file editor

Documentation for the above tasks can be found under [Getting Started](./)
## Hello World

For this example, create a file called `~/hello_world.sh` with the following
content:

```bash
#!/bin/bash
#SBATCH -n 1
#SBATCH --mem=2G
echo "Hello World!"
```

### What do the lines mean?

1) `#!/bin/bash` This is a [shebang] it tells Linux how to handle the file.
Here's we're saying use `bash` to run this file
2) `#SBATCH -n 1` This is a SLURM directive asking for 1 task
3) `#SBATCH --mem=2G` Now we're asking for 2 gigabytes of memory. Notice the
suffix `G`, the default suffix is `M`, but we can also use `K` or `T`
4) `echo "Hello World!"` This is the command that gets run on the compute node

For more SLURM directives, see `man sbatch` or the documentation for [sbatch].

[shebang]: https://en.wikipedia.org/wiki/Shebang_(Unix)
[sbatch]: https://slurm.schedmd.com/sbatch.html

### Submitting the Job

To submit the job, run the following command: `sbatch ~/hello_world.sh`.

```shell
> sbatch ~/test.sh
Submitted batch job 2970359

```

Check the job's status in the queue using: `squeue -u $(whoami)`.

```shell
> squeue -u $(whoami)
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           2970359       gpu hello_wo  awadell PD       0:00      1 (None)

```

> The `-u $(whoami)` flag cause `squeue` to only show jobs for the current user.
> Omitting this will show the entire queue.

The `squeue` command displays the current state of SLURM's queue and by default
the following columns:

| Name | Description |
|------|-------------|
| JOBID     | The numerical id SLURM uses to identify a job |
| PARTITION | The partition the job was submitted to |
| USER      | Who submitted the job |
| ST        | The state of the job, see the docs for a list of abbreviations |
| TIME      | How long the job has been running for |
| Nodes     | How many nodes the job is running on |
| NODELIST(REASON) | Why the job isn't running or a list of the nodes it's running on |

For more information on `squeue` checkout `man squeue` or it's
[documentation](https://slurm.schedmd.com/squeue.html).

### Getting Results

Once the job has completed (It will disappear from the output of `squeue`) we
should be left with a `slurm-<jobid>.out` file (Replace `<jobid>` with your `JOBID`).
Displaying this file should give the following:

```shell
> cat slurm-2970359.log
Hello World!

```

> By default SLURM will create this file, but you can change it's name via
> `#SBATCH -output` directives or `sbatch`'s command line flags `--output`.
> See [sbatch] for more information.

[sbatch]: https://slurm.schedmd.com/sbatch.html

This file will contain the [standard output] of the script `~/hello_world.sh`.
Job scripts are not limited to just this file. Output can be saved to other files
like this:

```bash
#!/bin/bash
#SBATCH -n 1
#SBATCH --mem=2G
echo "Hello World!" > ~/another_file.txt
```

This will instead write "Hello World!" to `~/another_file.txt` instead of
`slurm-<jobid>.out`. Slurm will still create a `slurm-<jobid>.out` file, but now
it will now be empty.

> The `>` tells bash we what to redirect the output of `echo` to `~/another_file.txt`.
> Check out [Redirection] for more information

[standard output]: https://en.wikipedia.org/wiki/Standard_streams
[Redirection]: https://www.gnu.org/software/bash/manual/html_node/Redirections.html

## What's Next?

- [Job Arrays] for submitting lots of similar jobs
- [Heterogenous Jobs] for submitting jobs made up of multiple job steps

[Job Arrays]: https://slurm.schedmd.com/job_array.html
[Heterogenous Jobs]: https://slurm.schedmd.com/heterogeneous_jobs.html
