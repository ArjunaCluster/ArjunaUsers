import subprocess
import logging
import math
import re
from datetime import datetime, time, timedelta
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
    elif str == "UNLIMITED":
        return np.inf
    else:
        return None
    return timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    ).total_seconds()


USAGE_REGEXP = re.compile(r"([\d\.]+)(\w+)")


def parse_bytes(str):
    """ Convert du human readable usage into bytes 1K -> 1024 """
    m = USAGE_REGEXP.match(str)
    if m:
        number = float(m.group(1))
        unit = m.group(2)
        unit_idx = ["K", "M", "G", "T", "P", "E", "Z", "Y"].index(unit)
        return float(number) * 1024 ** (unit_idx + 1)
    else:
        return float(str)


JOB_ID_SPLIT = re.compile(r"[\.+_]")


def __norm_jobid(str):
    return int(JOB_ID_SPLIT.split(str)[0])


def sacct():
    fields = [
        ("JobId", __norm_jobid),
        ("JobIdRaw", lambda x: x.split(".")[0]),
        ("User", str),
        ("Account", str),
        ("State", lambda x: "CANCELLED" if "CANCELLED" in x else x),
        ("Start", __parse_time),
        ("Submit", __parse_time),
        ("Elapsed", __parse_duration),
        ("Timelimit", __parse_duration),
        ("TotalCPU", __parse_duration),
        ("CPUTime", __parse_duration),
        ("MaxRSS", lambda x: parse_bytes(x) if x else 0),
        ("ReqMem", lambda x: {"mem": parse_bytes(x[0:-1]), "type": x[-1]}),
        ("NCPUS", int),
        ("NNodes", int),
        ("NTasks", lambda x: int(x) if x else None),
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
        df = pd.DataFrame.from_records(records)

    return __parse_reqmem(df)


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
    ax.set_xlabel("Queue Wait Time [hr]")
    ax.set_ylabel("Job Count")
    ax.set_xscale("linear")
    wait_times.to_csv("wait_time")


# Convert ReqMem to bytes
def __parse_reqmem(df):
    def tf(job):
        mem_bytes = job["ReqMem"]["mem"]
        mem_type = job["ReqMem"]["type"]
        if mem_type == "n":
            return mem_bytes * job["NNodes"]
        elif mem_type == "c":
            return mem_bytes * job["NCPUS"]
        else:
            LOG.warn("Got ReqMem type of %s for job %d", mem_type, job["JobId"])
            return mem_bytes

    df["ReqMemOut"] = df.apply(tf, axis=1)
    print(df)
    df["ReqMem"] = df["ReqMemOut"]
    return df


def plot_job_eff(ax, df) -> pd.DataFrame:
    # Extract Allocated Memory from ReqTRES and reduce to required columns
    job_eff = df.groupby("JobId").filter(lambda x: (~x.State.isin(["PENDING", "RUNNING"])).all())
    job_eff = job_eff[job_eff.CPUTime > 0]
    job_eff["MaxRSS"] = job_eff["MaxRSS"] * job_eff["NTasks"]
    job_eff = job_eff[
        ["User", "JobId", "JobIdRaw", "CPUTime", "TotalCPU", "ReqMem", "MaxRSS"]
    ]

    job_eff = job_eff.groupby(["JobId", "JobIdRaw"]).agg(
        {"CPUTime": "max", "TotalCPU": "max", "ReqMem": "max", "MaxRSS": "sum"}
    )
    job_eff = job_eff.groupby("JobId").agg(
        {"CPUTime": "sum", "TotalCPU": "sum", "ReqMem": "sum", "MaxRSS": "sum"}
    )

    # Compute Efficiencies
    job_eff["cpu_eff"] = 100 * (job_eff.TotalCPU / job_eff.CPUTime)
    job_eff["mem_eff"] = 100 * (job_eff.MaxRSS / job_eff.ReqMem)

    # Plot CPU Efficiencies
    job_eff["cpu_eff"].hist(
        ax=ax[0],
        bins=25,
        range=(0, 100),
        grid=False,
        log=True,
    )
    ax[0].set_xlabel("CPU Efficiency [%]")
    ax[0].set_ylabel("Job Count")

    # Plot Memory Efficiencies
    job_eff["mem_eff"].hist(
        ax=ax[1],
        bins=25,
        range=(0, 100),
        grid=False,
        log=True,
    )
    ax[1].set_xlabel("Memory Efficiency [%]")
    ax[1].set_ylabel("Job Count")

    # Return for further processing
    return job_eff


def plot_time_eff(ax, df):
    time_eff = df[
        ~df.Timelimit.isnull() & ~df.State.isin(["PENDING", "RUNNING", "CANCELLED"])
    ]
    time_eff = time_eff[["User", "JobId", "Elapsed", "Timelimit"]]
    time_eff["time_eff"] = 100 * (time_eff.Elapsed / time_eff.Timelimit)

    time_eff["time_eff"].hist(
        ax=ax,
        bins=25,
        range=(0, 100),
        grid=False,
        log=True,
    )
    ax.set_xlabel("Time Efficiency [%]")
    ax.set_ylabel("Job Count")
    return time_eff


if __name__ == "__main__":
    df = sacct()
    df.to_csv("sacct.csv")

    fig, axes = plt.subplots(nrows=2, ncols=2)

    # Plot Wait Times
    plot_wait_times(axes[0, 0], df)

    # Plot Time Efficiencies
    time_eff = plot_time_eff(axes[0, 1], df)
    time_eff.to_csv("time_eff.csv")

    # Compute CPU/Memory Efficiency
    job_eff = plot_job_eff(axes[1], df)
    job_eff.to_csv("job_eff_out.csv")

    # Save Dashboard
    fig.tight_layout()
    plt.savefig("queue_time.png")

    # Get User Job Efficiency
    job_users = (
        df[df.User.notnull()][["JobId", "User"]]
        .groupby("JobId")
        .aggregate(lambda x: x.unique()[0])
    )
    user_job_eff = job_eff.join(job_users, on="JobId")
    user_job_eff = user_job_eff.groupby("User").agg(
        {"CPUTime": "sum", "TotalCPU": "sum", "MaxRSS": "sum", "ReqMem": "sum"}
    )
    user_job_eff["cpu_eff"] = user_job_eff.TotalCPU / user_job_eff.CPUTime
    user_job_eff["mem_eff"] = user_job_eff.MaxRSS / user_job_eff.ReqMem

    # Get User Time Efficiency
    user_time_eff = (
        time_eff[~np.isinf(time_eff["Timelimit"])]
        .groupby("User")
        .agg({"Elapsed": "sum", "Timelimit": "sum"})
    )
    user_time_eff["time_eff"] = user_time_eff["Elapsed"] / user_time_eff["Timelimit"]

    # Write to markdown
    user_stats = user_job_eff[["TotalCPU", "cpu_eff", "mem_eff"]]
    user_stats = user_stats.merge(
        user_time_eff["time_eff"],
        how="outer",
        left_index=True,
        right_index=True,
    )
    user_stats.sort_values("TotalCPU", ascending=False, inplace=True)
    user_stats["TotalCPU"] = user_stats["TotalCPU"].map(
        lambda x: f"{x:8.3G}" if ~np.isnan(x) else ""
    )
    for k in user_stats.keys():
        if "eff" in k:
            user_stats[k] = user_stats[k].map(
                lambda x: f"{x:3.1%}" if ~np.isnan(x) else ""
            )
    user_stats.rename(
        columns={
            "TotalCPU": "Core-hours",
            "cpu_eff": "CPU Eff. [%]",
            "mem_eff": "Memory Eff. [%]",
            "time_eff": "Time Eff. [%]",
        },
        inplace=True,
    )
    user_stats.to_csv("user_stats.csv")
    with open("user_stats.md", "w") as io:
        user_stats.to_markdown(io, tablefmt="github")
