---
title: Data Backup
layout: default
parent: Getting Started
nav_order: 4
---

# Data Backup

While data storage on Arjuna is [configured](../about/hardware.md#storage) to provide robustness against
disk failure, [disaster can strike](https://lists.andrew.cmu.edu/mailman/private/arjuna-users/2021-September/000050.html).
Users are responsible for **backing up their data reguarly**, _especially_
things that take a lot of (human or computer) time to reproduce!
This guide will cover transferring files to and from Arjuna and configuring automated backups.
Users may need to use a variety methods to meet their backup/file transfer needs.

> We **STRONGLY RECOMMEND** users configure [automated backups](#automated-backups)

[RAID]: https://en.wikipedia.org/wiki/RAID

## Grabbing a single file: `scp`

If you just need to move a single file/directory onto/off of Arjuna, the easiest approach is the `scp` command, which has identical syntax to `cp`, but for remote systems requires a full specification of the file's location, for example:

```bash
# copy a file from arjuna to local machine
scp username@arjuna.psc.edu:~/src_dir/myfile ~/dest_dir/

# copy a file from local machine to arjuna
scp myfile username@arjuna.psc.edu:~/dest_dir/
```

These commands can be shortened to `scp arjuna ~/src_dir/myfile ~/dest_dir/` by
setting up an [SSH config file](../getting_started/connecting.md#using-a-ssh-config-file).

## Managing code: GitHub

For scripts and other code, version control via [git] and cloud syncing to [GitHub] is a good solution. Many good tutorials on this can be found via Google, and we've suggested some [over here] as well.

[git]: https://git-scm.com
[GitHub]: https://github.com
[over here]: ../getting_started/linux.md#git

## Transferring Multiple Files

Suppose you want to back up the entire contents of your home directory. You could periodically `scp -r` to a location on your local machine. However, this is inefficient as many files may not have changed at all, and also may use up more local disk space than you'd like. Both of these issues can be ameliorated by other solutions:
* The `rsync` command is similar to `scp`, but it will compare sizes and modification times of files to _only copy files that have been updated_. Basic syntax is `rsync source destination`
* `rclone` is similar to `rsync`, but allows syncing files with cloud storage services such as Google Drive or Box

An easy, "set-it-and-forget-it" solution to periodically back up your entire home directory to a cloud service using [`rclone`](https://rclone.org). As a CMU affiliate, you get access to unlimited storage space on Google Drive as well as 1TB on Box. The next sections detail how to configure these as remotes for `rclone`, as well as setting up a cron job to automatically run backups for you on a schedule.

### Setting up `rclone` remotes

`rclone` requires configuration of remote destinations to which it can sync files. It comes with an interactive walkthrough for setting these up. Start by running `rclone config`. The ensuing steps in the interactive prompt should look something like:
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

You will probably want to create a folder on your remote (GDrive or Box) in which your backups will live. Let's suppose you've done that and it's called `arjuna_backup`, and that the name of your remote is `gdrive_cmu` (if you don't remember what you called it, run `rclone listremotes`).

Assuming you are in your home directory and you want to back up the entire thing, the syntax would then be
```bash
rclone sync -P . my_remote:arjuna_backup
```
The `-P` flag isn't necessary, but it will give you progress updates. You may get a bunch of warnings about symlinks not being copied.

Note that for your first backup, if you have a lot of stuff in your directory, it may take a long time to run, and could get interrupted if your internet connection cuts out. `tmux` is a useful tool to get around this and keep tasks running even if you disconnect (many good tutorial easily found on Google).

### Automated Backups

A generic cron job to run backups is provided below, to use it do the following:

1. Create a file `~/backup.sh` with the indicated contents.
2. Run `crontab -e`
3. In the editor that opens, add the following line to the bottom of the file:
   `0 0 1 * * bash ~/backup.sh`
4. Trigger the first backup manually: `bash ~/backup.sh`
5. The next back will occur at 0:00 on the first day of the month.
   *CHECK THAT THIS IS HAPPENS!*

> Users are responsible for backing up their data, verifying their backups,
> and the operation of any backup scripts. *INCLUDING THIS ONE*!

#### Contents of `~/backup.sh`

```bash
#!/bin/bash
# A script to back up user folders on Arjuna
# For more information vist:
# https://arjunacluster.github.io/ArjunaUsers/getting_started/lindata_backup.html

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Replace "my_remote" with the name of your remote
# Replace "arjuna_backup" with the name of the folder you want to backup to on
# your remote
# Add additional filters (See https://rclone.org/filtering/) as needed
# NOTE: Be sure to "quote" your filters and append each line with "\"
#
# To "Dry Run" syncing (And quickly check what will be synced), replace the
# first line with: `rclone sync -P --dry-run gdrive-cmu:arjuna_backup \`
rclone sync -P ~ gdrive-cmu:arjuna_backup --dry-run \
    --ignore-case \
    --filter "- /.cache/**" \
    --filter "- /.bash_history" \
    --filter "- .git/**" \
    --filter "- .spack-env/**" \
    --filter "+ .spack/*.yml" \
    --filter "- .spack/**" \
    --filter "- __pycache__/**" \
    --filter "- *.py[cod]" \
    --filter "- .ipynb_checkpoints/**" \
    --filter "+ .julia/config/**" \
    --filter "+ .julia/prefs/**" \
    --filter "+ .julia/environments/**" \
    --filter "- .julia/**" \
    --filter "- .vscode-server/**" \
    --filter "+ *" \

```

#### Restrictions on Backups

Please be cognizant of other users when configuring your backup scripts. Daily
backups are *strongly discouraged* due to the strain it puts on the file system.
Please try to keep automated backups to within the following limits:

| Backup Rate | Max Backup Size [GB] |
| ----------- | -------------------- |
| Daily       | 5                    |
| Weekly      | 45                   |
| Monthly     | 150                  |

> This is intended to be a guideline for *automated* backups, and not one time
> transfers of data. Excessive backups puts strain on the file system and *may be
> throttled*.
