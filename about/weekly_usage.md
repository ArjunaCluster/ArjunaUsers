---
layout: default
title: Weekly Usage
parent: About Arjuna
nav_order: 3
---

![Usage]({{ site.baseurl }}/img/weekly_usage.png "Weekly Usage Charts")

The above plot shows the distribution of the following parameter of the previous week.

<dl>
  <dt>Queue Wait Time</dt>
  <dd>The amount of time a job waited in the queue before starting</dd>
  <dt>Time Efficiency</dt>
  <dd>The ratio of a job's requested time limit to it's wall time</dd>
  <dt>CPU Efficiency</dt>
  <dd>The ratio of a job's requested core-hours to it's usage</dd>
  <dt>Memory Efficiency</dt>
  <dd>The ratio of a job's requested memory to it's usage</dd>
</dl>

## Usage Efficiencies

Low efficiencies for CPU, Memory and Time negatively impacts SLURM's ability to
allocated resources to jobs, and can delay a jobs start time.

For example, consider a job requesting a Timelimit of 7 days, but typically
completes in an hour. SLURM will not schedule that job if a one-hour window
is available and instead will delay the job until a seven-day window opens up.

Or consider a job that requests 32 GB of memory but only uses 1 GB. This has
the following negative impacts:

- The TRES of that jobs will be larger, reducing the User's fair-share priority for future jobs
- SLURM will delay starting the job until sufficient resources are available
- It prevents other jobs from utilizing those resource

It is important to note that higher, not perfect, cluster utilization is the
goal. Less than 100% utilization for CPU, Memory or Time, is expected. Some jobs
are memory-bound, while others are compute-bound, and estimating a job's time limit
is often tricky.

Users should aim to refine their job's requested allocations based on the
requirements of similar previous jobs.

## User Usage

{% include user_stats.md %}

## Methodology

Statistics are computed for jobs that finished in the past weeks. At present,
canceled jobs are excluded from the Time Efficiency statistics.

Additionally, user averages are reported for the above parameters, as well as,
core-hours in the past week, and user disk usage. Jobs with an "UNLIMITED" time
limit are excluded from the User's average time efficiencies.
