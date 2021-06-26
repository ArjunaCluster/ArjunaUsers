---
layout: default
title: Cluster Architecture
parent: About Arjuna
nav_order: 1
---

# Cluster Architecture

## Head Node

When you ssh into Arjuna you are connected to the Head Node. This machine is
for used for transferring file to/from Arjuna and submitting jobs to the cluster.
The Head Node does have internet access.

> Do not run compute jobs on the head node! This include Jupyter Notebooks

The head node is a multi-user environment, please be cognizant of how your actions
(heavy compute, downloading large files, lots of IO) can impact other users.

## Compute Nodes

Arjuna has the following compute nodes available for usage

- 70 CPU nodes, each with 128 GB memory and 56 cores
- 2 high-memory nodes, each with 512 GB memory and 32 cores
- 27 GPU nodes, each with 128 GB memory, 64 cores, and 4 K80 NVIDIA GPUs

Compute Nodes do not have access to the internet.

## RAID Storage

Arjuna has a 20 TB of [RAID 0] storage for the entire cluster. This filesystem
is not backed up and has no redundancy or fault tolerance. ***A single disk failure
will result in a total loss of data.***

> Long term storage of data on Arjuna is not recommended. Please store important
> or critical data elsewhere.

[RAID 0]: https://en.wikipedia.org/wiki/Standard_RAID_levels#RAID_0

Weekly disk usage emails are sent out via the list serve. Please be mindful
of your usage, and remove files when they are not longer needed.

The following command will remove all files in your home directory with a given
type (This example will remove `*.gpw` files)

```shell
find ~ -name `*.gpw` -delete
```

# Partitions
