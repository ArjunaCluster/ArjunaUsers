---
title: Running Jupyter Notebooks with Visual Studio Code
layout: default
parent: Getting Started
nav_order: 6
---

# Running Jupyter Notebooks with Visual Studio Code

Jupyter Notebooks offer a convenient way to to interactively work on something but can have a heavy computational workload and are thus prohibited from running on the head node. [See the Acceptable Use Policy](../about/accounts.md#acceptable-use-policy). You should run notebooks on the worker nodes instead as described in this tutorial.

For using Jupyter Notebooks you will need to have:
1. Visual Studio Code installed on your local machine with [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python), [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) and [Remote SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extensions enabled. You should be able to successfully run a python script from within Visual Studio Code on arjuna first.
2. Jupyter notebook installed in your environment e.g. via a conda environment on arjuna.
```
conda create -n my_env
conda install python
conda install -c conda-forge notebook
conda install -c conda-forge nb_conda_kernels
```


### Instructions
1. Allocate an interactive worker node with the resources you need, for example:
```
srun -N 1 -n 1 -A <account> -p <partition> --mem=2G -t 01:00:00 --pty bash
```
or if you need a GPU:
```
srun -N 1 -n 1 -A <account> -p gpu --gres=gpu:1 --mem=2G -t 01:00:00 --pty bash
```
with the appropriate account and [partition](../about/hardware#partitions). 

> Be reasonable about your needs. If you are not running any parallelized code, you will need 2 cores at most, if you don't need a GPU, don't request it. The time requested should be a reflection of how long you will actually work on the node.

> Jupyter can only run on a single machine. Be sure to specify `-N 1`

2. In the worker node, activate the environment with jupyter installed that you want to use and start the notebook server e.g. in conda:
```
conda activate my_env
jupyter notebook --ip $(hostname) --no-browser
```
After the wall of text, identify the server url containing the ip address of the worker node, something like:
```
http://c022:8888/?token=a6935b8b842eb4d6916ea36dd76c7bf3d21c8c909f26aab1
```
where `c022` is the hostname of the worker node. Copy it.

3. Start up Visual Studio Code and choose the server you just started. Do this by opening the command palette (usually `Cmd+Shift+P`) and search for `Jupyter: Select Jupyter Server for Connections`. Enter the url from step 2.

4. Open your notebook and write your code
