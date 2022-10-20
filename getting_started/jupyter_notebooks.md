---
title: Running Jupyter Notebooks with VS Code
layout: default
parent: Getting Started
nav_order: 6
---

# Running Jupyter Notebooks with VS Code

Jupyter Notebooks offer a convenient way to to interactively work on something but can have a heavy computational workload and are thus prohibited from running on the head node. You should run notebooks on the worker nodes instead as described in this tutorial.

For this workflow you will need to have:
1. VS Code installed on your local machine with Python, Jupyter and Remote SSH extensions enabled. You should be able to successfully run a python script from within VS code on arjuna first
2. Jupyter installed in your environment e.g. via a conda environment on arjuna.


### Instructions
1. Allocate an interactive worker node with the resources you need, for example:
```
srun -N 1 -n 1 -A <account> -p <partition> --mem=2G -t 01:00:00 --pty bash
```
or if you need GPUs:
```
srun -N 1 -n 1 -A <account> -p gpu --gres=gpu:1 --mem=2G -t 01:00:00 --pty bash
```
with the appropriate account and partition. Be reasonable about your needs. If you are not running any parallelized code, you will need 2 cores at most, if you don't need a GPU, don't request it. The time requested should be a reflection of how long you will actually work on the node.

2. In the worker node, activate the conda environment with jupyter installed that you want  to use and start the notebook server:
```
conda activate my_env
jupyter notebook --ip $(hostname) --no-browser
```
After the wall of text, identify the server url containing the ip address of the worker node, something like:
```
http://c022:8888/?token=a6935b8b842eb4d6916ea36dd76c7bf3d21c8c909f26aab1
```
where `c022` is the hostname of the worker node. Copy it.

3. Start up VS Code and choose the server you just started. Do this by opening the command palette (usually `Cmd+Shift+P`) and search for `Jupyter: Select Jupyter Server for Connections`. Enter the url from step 2.

4. Open your notebook and write your code

> Note 1: VS Code does not automatically save notebooks so you will have to keep saving your work. If your wall time runs out before you save, you will have to restart the server and save again.

> Note 2: Running the notebook as above is really slow. If your use case uses small amounts of data and does not require special hardware, you might be better off mounting your Arjuna home directory locally on your machine using something like [FUSE](https://susanqq.github.io/jekyll/pixyll/2017/09/05/remotefiles/) and running your server locally.
