---
title: Data Backup
layout: default
parent: Getting Started
nav_order: 3
---

# Data Backup

While data storage on Arjuna is [RAID] configured to provide robustness against disk failure, disaster can strike (and did, RIP a lot of things 2021), so it's individual users' responsibility to **back up your data regularly**, _especially_ things that would take a lot of (human and/or computer) time to reproduce! There are a few approaches you can take to do this (outlined on this page), and you will likely want to choose a combination of them for various types of files/code/data. **We strongly recommend that users configure backups to run in a scheduled, automatic fashion** (e.g. using cron jobs) to avoid the need to remember to back up and the possibility of attendant data loss. Instructions to set this up are provided below.

[RAID]: https://en.wikipedia.org/wiki/RAID

## Grabbing a single file: `scp`
If you just need to move a single file/directory onto/off of Arjuna, the easiest approach is the `scp` command, which has identical syntax to `cp`, but for remote systems requires a full specification of the file's location, for example:

```bash
# copy a file from arjuna to local machine
scp username@arjuna.psc.edu:/home/username/src_dir/myfile ~/dest_dir/

# copy a file from local machine to arjuna
scp myfile username@arjuna.psc.edu:/home/username/dest_dir/
```

(It may be useful to set up aliases to avoid having to type out the full locations)

## Managing code: GitHub
For scripts and other code, version control via git and cloud syncing to GitHub is a good solution. Many good tutorials on this can be found via Google.

## Other data
Suppose you want to back up the entire contents of your home directory. You could periodically `scp -r` to a location on your local machine. However, this is inefficient as many files may not have changed at all, and also may use up more local disk space than you'd like. Both of these issues can be ameliorated by other solutions:
* The `rsync` command is similar to `scp`, but it will compare sizes and modification times of files to _only copy files that have been updated_. Basic syntax is `rsync source destination`
* `rclone` is similar to `rsync`, but allows syncing files with cloud storage services such as Google Drive or Box

An easy, "set-it-and-forget-it" solution to periodically back up your entire home directory to a cloud service using `rclone`. As a CMU affiliate, you get access to unlimited storage space on Google Drive as well as 1TB on Box. The next sections detail how to configure these as remotes for `rclone`, as well as setting up a cron job to automatically run backups for you on a schedule.

### Setting up `rclone` remotes
`rclone` requires configuraiton of remote destinations to which it can sync files. It comes with an interactive walkthrough for setting these up. Start by running `rclone config`. The ensuing steps in the interactive prompt should look something like:
1. Press `n` for a new config
2. Enter a name for it, e.g. "Box" or "GDrive"
3. Enter the number associated with the type of remote (as of 11/8/21, Box was 6 and Google Drive was 15)
4. Now the procedure bifurcates a bit...

#### Google Drive
5. You should have gotten a link to [this page](https://rclone.org/drive/#making-your-own-client-id). Follow the instructions to create a client id. One gotcha here is that **you won't be able to do this while logged into your andrew.cmu.edu** GSuite account, because you won't have permissions to create a project in that organization, so make sure to do it with a personal Google ID. (Don't worry, you'll still be able to link it to your Andrew GDrive space later) 
6. You should eventually get a client ID and secret that you can paste into the `rclone` prompt to continue configuring. 
7. Provide full access (option 1) at the `scope` prompt.
8. Continue with default options until the question "Use auto config?" Because we are on a remote machine, you should enter `n` for this. 
9. You will get a link at which you should authenticate with your Google account. **At this step, be sure to use your Andrew account if that's where you want to back up!"** You may get a warning, proceed anyway (in a Chrome browser, by clicking Advanced and then "go to rclone"). 
10. After authenticating, copy the code and paste into the rclone prompt.
11. From here, you should be able to continue with default options and finish configuring! Phew!

#### Box
5. Follow default options until the "use auto config?" prompt. Because we are on a remote machine, you should enter `n` for this. 
6. You will then need to open a local terminal session to access your web browser for authentication. Follow the instructions to do so.
7. After authentication, on your local terminal, you should get something to paste into your remote session. Make sure to copy everything between the arrows.
8. Follow defaults to finish configuration.

### Running an `rclone` backup
You will probably want to create a folder on your remote (GDrive or Box) in which your backups will live. Let's suppose you've done that and it's called `arjuna_backup`, and that the name of your remote is `my_remote` (if you don't remember what you called it, run `rclone listremotes`).

Assuming you are in your home directory and you want to back up the entire thing, the syntax would then be
```bash
rclone sync -P . my_remote:arjuna_backup
```
The `-P` flag isn't necessary, but it will give you progress updates. You may get a bunch of warnings about symlinks not being copied.

Note that for your first backup, if you have a lot of stuff in your directory, it may take a long time to run, and could get interrupted if your internet connection cuts out. `tmux` is a useful tool to get around this and keep tasks running even if you disconnect (many good tutorial easily found on Google).

### Scheduling backups
add some stuff about how to do it with a cron job