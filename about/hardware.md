---
layout: default
title: Cluster Architecture
parent: About Arjuna
nav_order: 1
---

# Cluster Architecture

## Head Node

When you ssh into Arjuna, you connect to the "Head Node", also known as c001. From this machine, you
can do the following

- Transfer files to/from Arjuna to a local machine (ie a compute node or another computer connected to the CMU network to which you have access)
- Download files from the internet
- Submit jobs to the cluster
- Monitor the status of existing jobs

**DO NOT** run compute jobs on the head node. Moreover, do not use the headnode for anything other than submitting jobs to compute nodes. Unauthorized uses of the head node include, but are not limited to:
- Running Jupyter Notebooks to analyze data
- Webscraping
- Running Simulations

Authorized uses of the headnode include, but are not limited to:
- Installing software for use on the compute nodes
- Moving data to and from Arjuna
- Submitting jobs

If the desired compute task is anything other than trivial operations required for job submission which can only be run on the headnode of arjuna, it should be run on a worker node or elsewhere.

## Compute Nodes

Arjuna has the following compute nodes available for usage

- 58 CPU nodes, each with 128 GB memory and 56 cores d[001-032],f[001-024],e[001-002]
- 2 high-memory nodes, each with 512 GB memory and 32 cores e[003-004]
- 27 GPU nodes, each with 128 GB memory, 64 CPU cores, and 4 K80 NVIDIA GPUs c[002-028]

The Headnode (c001) has the same hardware as a GPU node. However, do not use the headnode to run anything.

## RAID Storage

Arjuna has 20 TB of [RAID 6] storage. 

> Arjuna's RAID Storage is not for long-term storage of data. Please use other resources, such as CMU's unlimited google drive access, to store data for long term.

[RAID 6]: https://en.wikipedia.org/wiki/Standard_RAID_levels#RAID_6

Weekly disk usage emails are sent out via the list-serve. Please be mindful of your usage, and promptly remove unused files. Users should never exceed 500GB of storage. Files which are not required to be on the cluster should be promptly removed. 

The following command will remove all files in your home directory with a given
type (This example will remove `*.gpw` files)

```shell
find ~ -name `*.gpw` -delete
```

