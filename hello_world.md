# Submitting Your First Job

This tutorial will guide you through the process of submitting your first job on
Arjuna. This tutorial assumes you've already done the following items

1) Login to Arjuna via `ssh`
2) Some familiarity with entering commands at a `bash` shell
3) Some familiarity with `vim` or another command line file editor

Checkout [Intro to Linux] for some help with the above topics.

[Intro to Linux]: linux.md

## Hello World

For this example create a file called `~/hello_world.sh` with the following
content:

```bash
#!/bin/bash
#SBATCH --cpus=1
#SBATCH --mem=2G
echo "Hello World!"
```

### What do the lines mean?

1) `#!/bin/bash` This is a [shebang] it tells linux how to handle the file.
Here's we're saying use `bash` to run this file
2) `#SBATCH --cpus=1` This is a SLURM directive asking for 1 CPU
3) `#SBATCH --mem=2G` Now we're asking for 2G of Memory in bytes. Notice the
suffix `G`, the default is `M` but we can also use `K` or `T`
4) `echo "Hello World!"` This is command that we're actually running

For more SLURM directive checkout `man sbatch` or the documentation for [sbatch].



[shebang]: https://en.wikipedia.org/wiki/Shebang_(Unix)
[sbatch]: https://slurm.schedmd.com/sbatch.html

### Submitting the Job

To submit our job we no run the following command: `sbatch ~/test.sh`.
You should see something like the following:

```shell
> sbatch ~/test.sh
Submitted batch job 2970359

```

Check that status of your job in the queue using: `squeue -u $(whoami)`.
You should get something similar to the following:

```shell
> squeue -u $(whoami)
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           2970359       gpu hello_wo  awadell PD       0:00      1 (None)

```

The `squeue` command lets you look at the state of SLURM's que
(The jobs you and other have submitted to it).

| Name | Description |
|------|-------------|
| JOBID     | The numerical id SLURM uses to identify a job |
| PARTITION | The partition the job was submitted to |
| USER      | Who submitted the job |
| ST        | The state if the job, check the docs for a list of abbreviations |
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
> `#SBATCH` directives or command line flags to `sbatch`


This file will contain the [standard output] of our script `~/hello_world.sh`,
but we're not limited to just this file. We could also write to a different file,
like this:

```bash
#!/bin/bash
#SBATCH --cpus=1
#SBATCH --mem=2G
echo "Hello World!" > ~/another_file.txt
```

This will instead write "Hello World!" to `~/another_file.txt` instead of `slurm-<jobid>.out`.
Note: this will still create a `slurm-<jobid>.out`, but now it will be an empty file.

> This uses [Redirection] (The `>` symbol) to create the other file, but you're
> not limited to this

[standard output]: https://en.wikipedia.org/wiki/Standard_streams
[Redirection]: https://www.gnu.org/software/bash/manual/html_node/Redirections.html

## What's Next?

- [Job Arrays]: For submitting lots of similar jobs
- [Heterogenous Jobs]: For submitting jobs made up of multiple job steps

[Job Arrays]: https://slurm.schedmd.com/job_array.html
[Heterogenous Jobs]: https://slurm.schedmd.com/heterogeneous_jobs.html
