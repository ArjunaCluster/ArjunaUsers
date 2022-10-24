---
title: Running Jupyter Notebooks with Visual Studio Code
layout: default
parent: Getting Started
nav_order: 6
---

# Running Jupyter Notebooks with Visual Studio Code

Jupyter Notebooks offer a convenient way to interactively work on something,
but can be a heavy computational workload and are
[prohibited from running on the head node](../about/accounts.md#acceptable-use-policy).
You must run notebooks on the worker nodes, as described, in this tutorial.

> Notebooks run on the headnode may be terminated without warning

For using Jupyter Notebooks you will need to have:

1. Visual Studio Code installed on your local machine with [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python), [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) and [Remote SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extensions enabled.
2. Installed Jupyter notebook on Arjuna (i.e. via [conda](https://docs.conda.io/en/latest/) or [spack](https://spack.readthedocs.io/en/latest/))

### Instructions
1. Allocate an interactive worker node with the resources you need, for example:

```bash
# Request 1 cpu with 2G of memory for 1 hour
srun -N 1 -n 1 -A <account> -p <partition> --mem=2G -t 01:00:00 --pty bash

# The same, but with a gpu:
srun -N 1 -n 1 -A <account> -p gpu --gres=gpu:1 --mem=2G -t 01:00:00 --pty bash
```
Replace `<account>` and `<partition>` with the appropriate account and
[partition](../about/hardware#partitions).

> Interactive sessions do count against your
> [fairshare](../getting_started/slurm_intro.md#accounting). Generally 2 cores
> is sufficient for non-parallelized codes.
> __Jupyter can only run on a single machine__. Be sure to specify `-N 1`

2. On the worker node, launch the notebook server: `jupyter notebook --ip
   $(hostname) --no-browser`

After the wall of text, identify the server url containing the ip address of the
worker node, something like:

```
http://c022:8888/?token=a6935b8b842eb4d6916ea36dd76c7bf3d21c8c909f26aab1
```

where `c022` is the hostname of the worker node. Copy it.

3. Start up Visual Studio Code and choose the server you just started. Do this
   by opening the command palette (usually `Cmd+Shift+P`) and search for
   `Jupyter: Select Jupyter Server for Connections`. Enter the url from step 2.

4. Open your notebook and write your code
