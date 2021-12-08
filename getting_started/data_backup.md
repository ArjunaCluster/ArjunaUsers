---
title: Data Backup
layout: default
parent: Getting Started
nav_order: 4
---

# Data Backup

While data storage on Arjuna is [configured](../about/hardware.md#storage) to provide robustness against
disk failure, [disaster can strike](https://lists.andrew.cmu.edu/mailman/private/arjuna-users/2021-September/000050.html).
Users are responsible for **backing up their data regularly**, _especially_
things that take a lot of (human or computer) time to reproduce!
This guide will cover transferring files to and from Arjuna and configuring automated backups.
Users may need to use a variety of methods to meet their backup/file transfer needs.

> We **STRONGLY RECOMMEND** users configure [automated backups](#automated-backups)

> Windows Users: `scp` and `rsync` are not installed by default on Windows.
> You will need to install them manually or use [WSL](https://docs.microsoft.com/en-us/windows/wsl/about)

[RAID]: https://en.wikipedia.org/wiki/RAID

## Small Transfers: `scp`

For small transfers (< 1GB) on to or off of arjuna, the following `scp` commands can be used from *your local machine*.

> Remember to replace `user` with your username

| Action                    | Command                                             |
| ------------------------- | --------------------------------------------------- |
| Copy a File from Arjuna   | `scp user@arjuna.psc.edu:path/to/file path/to/dst`  |
| Copy a File to Arjuna     | `scp path/to/file user@arjuna.psc.edu:path/to/dst`  |
| Copy a Folder from Arjuna | `scp -r user@arjuna.psc.edu:path/to/folder path/to` |
| Copy a Folder to Arjuna   | `scp -r path/to/folder user@arjuna.psc.edu:path/to` |

Notice when copying folders, the destination folder is `/path/to` not `/path/to/folder`.
`scp` will copy the folder to `/path/to` thus creating `/path/to/folder`; using a destination of `/path/to/folder` would result in `/path/to/folder/folder`.

These commands can be shortened to `scp arjuna:/path/to/file /path/to/dst` by
setting up an [SSH config file](../getting_started/connecting.md#using-a-ssh-config-file).
To read the manual page for `scp`, type `man scp` into a terminal.

## Managing Code

Source code tracked by [git] can be transferred via [GitHub] directly via ssh:

```bash
git clone git@github.com:ArjunaCluster/ArjunaUsers.git
```

See GitHub's documentation for connecting to [GitHub via ssh](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) for more information.

Additional resources for git and GitHub can be found on our [Other Resources](./linux.md#git) page.

[git]: https://git-scm.com
[GitHub]: https://github.com

## Larger Transfers: `rsync`

For larger file transfers (> 1GB or > 20 files), the following `rsync` commands can be used from *your local machine*.

> Remember to replace `user` with your username


| Action                    | Command                                             |
| ------------------------- | --------------------------------------------------- |
| Copy a File from Arjuna   | `rsync user@arjuna.psc.edu:path/to/file path/to/dst`  |
| Copy a File to Arjuna     | `rsync path/to/file user@arjuna.psc.edu:path/to/dst`  |
| Copy a Folder from Arjuna | `rsync -r user@arjuna.psc.edu:path/to/folder path/to` |
| Copy a Folder to Arjuna   | `rsync -r path/to/folder user@arjuna.psc.edu:path/to` |

Unlike `scp`, `rsync` checks files sizes and modification times to only transfer files that have changed. This is helpful for several reasons:

1. Resume interrupted transfers *without* repeating the entire transfer.
2. Reduce transfer times by *skipping* already transferred files.

To read the manual page for `rsync`, type `man rsync` into a terminal.

## Transfers to Cloud Storage: `rclone`

[`rclone`](https://rclone.org) can be used to transfer files to cloud storage providers (Google Drive, Box, Amazon S3, SFTP, [and more](https://rclone.org/overview/)). Unlike `scp` and `rsync`, `rclone` can be run from your local machine or arjuna, but requires additional configuration to operate.

### Installation Options

`rclone` is already installed on Arjuna, but you may need to install it on your local machine.
The following are possible ways to install `rclone` on your local machine:

- Download an installer from [rclone website](https://rclone.org/downloads/).
- If on MacOS, install with [homebrew](https://brew.sh/): `brew install rclone`

### Configuring `rclone` Remotes

`rclone` requires configuration of remote destinations ("Remotes") before it can sync files to them. To configure `rclone` use [`rclone config`](https://rclone.org/docs/#configure) to launch an interactive configuration tool. To add a new remote:

1. Press `n` for a new config.
2. Enter a name for the new remote (e.g. "box_cmu" or "gdrive_cmu").
3. Choosing the type of remote. (e.g. "Google Drive",  "Box", "S3", etc.).
4. Set remote-specific options.
5. Authenticate with the remote.

We have provided additional instructions for [Google Drive](#google-drive) and [Box](#box), but official documentation can be found on the [rclone website](https://rclone.org/overview/), by clicking "Storage Systems" and choosing the appropriate storage system.

#### Google Drive

After completing [steps 1 - 3 above](#configuring-rclone-remotes): you will be prompted to enter a [`client_id`](https://rclone.org/drive/#making-your-own-client-id)

1. When prompted from a [`client_id`](https://rclone.org/drive/#making-your-own-client-id), follow the instruction on the linked page.
    - *You must use a non-CMU account* due to institutional restrictions.
    - You *can* use this client id to sync with your Andrew GDrive account.
    - You can skip this step, but performance may be limited.

2. Paste your `client_id` and then `secret` when prompted by `rclone configure`.
3. The default options are fine until reaching "Use auto config?".
4. For "Use auto config?" enter `n` if configuring rclone on arjuna (Or another headless machine). Otherwise, enter `y`
5. Open the link in a browser (If you entered `y` above a browser window should open).
    - Choose the Google account to which you want to back up (i.e. your Andrew Account).
    - If using a personal client id, you may get a warning that "Google hasn't verified this app", click "Continue".

6. After authenticating, copy the code and paste it into the rclone prompt.
7. The remaining defaults should be fine.

#### Box

1. The default options are fine until reaching "Use auto config?".
2. For "Use auto config?" enter `n` if configuring rclone on arjuna (Or another headless machine). Otherwise, enter `y`.
3. Follow the instructions to authenticate with Box.
4. The remaining defaults should be fine.

### Syncing Files with `rclone`

To [sync](https://rclone.org/commands/rclone_sync/) a folder to a remote destination, use the `rclone sync` command:

```bash
# Local (Or from a teminal on Arjuna) to Remote
rclone sync -P path/to/folder remote:path/to/folder

# Remote to Local (Or from a teminal on Arjuna)
rclone sync -P remote:path/to/folder path/to/folder
```

The `-P` flag is used to enable progress reporting and will display real-time progress statistics. You may get warnings about symlinks not being copied. To copy symlinked files and folders, use the `--copy-links` flag.

Sometimes, `rclone` will take longer to back up than is practical to leave a terminal open on your computer. For these instances we recommend using a terminal multiplexer such as `tmux` or `screen`, both of which allow the user to detach from a terminal session. Do not attempt to back up via a slurm job!

> This is only applicable for non-automated backups.

## Automated Backups

A generic cron backup script is provided below; to use it, do the following:

1. Configure [rclone](#transfers-to-cloud-storage-rclone) for your cloud storage provider on Arjuna.
2. Create a file `~/backup.sh` with the [indicated contents](#contents-of-backupsh). Remember to replace `remote` with the name of your remote
3. Run `crontab -e`
4. In the editor that opens, add the following line to the bottom of the file:
   `0 0 1 * * bash ~/backup.sh > ~/backup.log 2>&1`
5. Trigger the first backup manually: `bash ~/backup.sh`
6. The next back will occur at 0:00 on the first day of the month.
   *CHECK THAT THIS HAPPENS!*

> Users are responsible for backing up their data, verifying their backups,
> and verifying the operation of any backup scripts. *INCLUDING THIS ONE*!

### Cron

`0 0 1 * * bash ~/backup.sh > ~/backup.log 2>&1` tells `crond` to run a command (`bash ~/backup.sh`)
at 0:00 on the first day of the month (`0 0 1 * *`), and pipe both [stderr and
stdout](https://en.wikipedia.org/wiki/Standard_streams) to `~/backup.log` For more information, on cron:

- See the man pages: `man cron`
- *Highly recommend*: [crontab guru](https://crontab.guru)

> Excessive cron usage will be throttled, please be mindful of other users

### Contents of `~/backup.sh`

```bash
#!/bin/bash
# A script to back up user folders on Arjuna
# For more information vist:
# https://arjunacluster.github.io/ArjunaUsers/getting_started/data_backup.html

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Replace "remote" with the name of your remote (i.e. gdrive_cmu)
# Replace "arjuna_backup" with the name of the folder you want to back up to on
# your remote
# Add additional filters (See https://rclone.org/filtering/) as needed
# NOTE: Be sure to "quote" your filters and append each line with "\"
#
# To "Dry Run" syncing (And quickly check what will be synced), replace the
# first line with: `rclone sync ~ --dry-run remote:arjuna_backup/current \`
rclone sync ~ remote:arjuna_backup/current \
    --backup-dir remote:"arjuna_backup/snapshot-$(date +%Y-%m-%d)" \
    --ignore-case \
    --filter "- /.cache/**" \
    --filter "- /.bash_history" \
    --filter "- .git/**" \
    --filter "+ .ssh/config" \
    --filter "- .ssh/**" \
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

This will sync most files in your home directory (`~`) to
`remote:arjuna_backup/current` and copy historical snapshots to `remote:arjuna_backup/snapshot-YYYY-MM-DD`
using [`--backup-dir](https://rclone.org/docs/#backup-dir-dir).
To sync other files, add or remove filters as needed.
See [rclone filtering](https://rclone.org/filtering/) for more information on
filters and how to use them.

### Restrictions on Backups

Please be cognizant of other users when configuring your backup scripts. Daily
backups are *strongly discouraged* due to the strain it puts on the file system.
Please try to keep automated backups within the following limits:

| Backup Rate | Max Backup Size [GB] |
| ----------- | -------------------- |
| Daily       | 5                    |
| Weekly      | 45                   |
| Monthly     | 150                  |

> This is intended to be a guideline for *automated* backups, and not one-time
> transfers. Excessive backups put unnecessary strain on the file system, and *may be
> throttled*.
