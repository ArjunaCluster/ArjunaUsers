---
layout: default
title: Cluster Architecture
parent: About Arjuna
nav_order: 1
---

# Cluster Architecture

## Head Node

When you ssh into Arjuna, you connect to the Head Node. From this machine, you
can do the following

- Transfer files to/from Arjuna to a local machine
- Download files from the internet
- Submit jobs to the cluster
- Monitor the status of existing jobs

> Do not run compute jobs on the head node

## Compute Nodes

Arjuna has the following compute nodes available for usage

- 70 CPU nodes, each with 128 GB memory and 56 cores
- 2 high-memory nodes, each with 512 GB memory and 32 cores
- 27 GPU nodes, each with 128 GB memory, 64 cores, and 4 K80 NVIDIA GPUs

## RAID Storage

Arjuna has a 20 TB of [RAID 6] storage for the entire cluster. 

> Arjuna's RAID Storage is not for long-term storage of data. Please use other resources, such as CMU's unlimited google drive access, to store data for long term.

[RAID 6]: https://en.wikipedia.org/wiki/Standard_RAID_levels#RAID_6

Weekly disk usage emails are sent out via the list-serve. Please be mindful
of your usage, and promptly remove unused files.

The following command will remove all files in your home directory with a given
type (This example will remove `*.gpw` files)

```shell
find ~ -name `*.gpw` -delete
```

# Partitions
