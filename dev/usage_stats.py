import subprocess
import logging
import math
import re
from datetime import datetime, timedelta
from typing_extensions import runtime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

logging.basicConfig()
LOG = logging.getLogger("stats")
LOG.setLevel(logging.DEBUG)


def __parse_time(str):
    try:
        return datetime.fromisoformat(str)
    except:
        return None


def __parse_duration(str):
    if "-" in str:
        str_split = str.split("-")
        days = int(str_split[0])
        str = str_split[1]
    else:
        days = 0

    hms = str.split(":")
    if len(hms) == 3:
        hours = int(hms[0])
        minutes = int(hms[1])
        seconds = float(hms[2])
    elif len(hms) == 2:
        hours = 0
        minutes = int(hms[0])
        seconds = float(hms[1])
    else:
        return None
    return timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    ).total_seconds()

RE_TRES = re,compile(r"(.*?)=([^,]*),?")
def __parse_tres(str):
    tres = {}
    for m in re.findall(str):
        tres[m.group(1)] = m.group(2)
    return tres

JOB_ID_SPLIT = re.compile(r"[\.+_]")


def __norm_jobid(str):
    return int(JOB_ID_SPLIT.split(str)[0])


def sacct():
    fields = [
        ("JobId", __norm_jobid),
        ("JobIdRaw", lambda x: x.split(".")[0]),
        ("User", str),
        ("Account", str),
        ("State", str),
        ("Start", __parse_time),
        ("Submit", __parse_time),
        ("Elapsed", __parse_duration),
        ("Timelimit", __parse_duration),
        ("TotalCPU", __parse_duration),
        ("CPUTime", __parse_duration),
    ]
    cmd = [
        "sacct",
        "-Pan",
        "--starttime 5/20/21",
        "--endtime 6/27/21",
        f"--format='{','.join([f[0] for f in fields])}'",
    ]
    LOG.debug(" ".join(cmd))
    """     proc = subprocess.Popen(
        " ".join(cmd), shell=True, stdout=subprocess.PIPE, encoding="UTF-8"
    ) """
    with open("sacct.out", "r") as io:
        records = __sacct_record(fields, io)
        return pd.DataFrame.from_records(records)


def __sacct_record(keys, stream):
    for line in stream:
        data = line.rstrip().split("|")
        yield {k: f(v) for ((k, f), v) in zip(keys, data)}


def filter_finalized(df):
    return df.groupby("JobId").filter(lambda x: (x.State == "COMPLETED").all())


def plot_wait_times(ax, df):
    wait_times = (df.Start - df.Submit).astype("timedelta64[h]")
    wait_times.where(~df.User.isnull(), inplace=True)
    wait_times.where(df.State != "PENDING", inplace=True)
    wait_times.where(~df.Start.isnull(), inplace=True)
    wait_times.hist(
        ax=ax,
        bins=20,
        grid=False,
        log=True,
    )
    ax.set_xlabel("Queue Wait Time [min]")
    ax.set_ylabel("Job Count")
    ax.set_xscale("linear")


def plot_job_eff(ax, df) -> pd.DataFrame:
    def cpu_efficency(job_steps):
        print(job_steps)
        cpu_alloc = job_steps.groupby("JobIdRaw").sum()
        cpu_used = job_steps.TotalCPU.sum()
        if cpu_alloc.seconds > 0:
            return cpu_used / cpu_alloc
        return None

    job_eff = df.groupby("JobId").filter(lambda x: (x.State == "COMPLETED").all())
    job_eff = job_eff[["User", "JobId", "JobIdRaw", "CPUTime", "TotalCPU"]]
    job_eff.to_csv("job_eff.csv")
    job_eff = job_eff.groupby(["JobId", "JobIdRaw"]).agg(
        {"CPUTime": "max", "TotalCPU": "max"}
    )
    job_eff = job_eff.groupby("JobId").agg({"CPUTime": "sum", "TotalCPU": "sum"})
    job_eff = job_eff[job_eff.CPUTime > 0]
    job_eff["cpu_eff"] = 100 * (job_eff.TotalCPU / job_eff.CPUTime)
    job_eff["cpu_eff"].hist(
        ax=ax,
        bins=25,
        range=(0, 100),
        grid=False,
        log=True,
    )
    ax.set_xlabel("CPU Efficiency [%]")
    ax.set_ylabel("Job Count")

    # Return for further processing
    return job_eff


if __name__ == "__main__":
    df = sacct()
    df.to_csv("sacct.csv")

    fig, axes = plt.subplots(nrows=1, ncols=2)

    # Plot Wait Times
    plot_wait_times(axes[0], df)

    # Compute CPU Efficiency
    job_eff = plot_job_eff(axes[1], df)
    job_eff.to_csv("job_eff_out.csv")

    # Save Dashboard
    fig.tight_layout()
    plt.savefig("queue_time.png")

    # Get User Job Efficiency
    job_users = (
        df[df.User.notnull() & df.Account.notnull()][["JobId", "User"]]
        .groupby("JobId")
        .aggregate(lambda x: x.unique()[0])
    )
    user_job_eff = job_eff.join(job_users, on="JobId")
    user_job_eff = user_job_eff.groupby("User").agg(
        {"CPUTime": "sum", "TotalCPU": "sum"}
    )
    user_job_eff["cpu_eff"] = 100 * (user_job_eff.TotalCPU / user_job_eff.CPUTime)

    # Write to markdown
    user_job_eff = user_job_eff[["cpu_eff"]]
    user_job_eff.sort_values("cpu_eff", ascending=False, inplace=True)
    user_job_eff.rename(columns={"cpu_eff": "CPU Eff. [%]"}, inplace=True)
    with open("user_job_eff.md", "w") as io:
        user_job_eff.to_markdown(io, floatfmt=".1f", tablefmt="github")
