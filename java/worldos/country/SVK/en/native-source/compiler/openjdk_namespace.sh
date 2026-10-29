#!/bin/sh
# Run only inside a fresh user/mount/PID namespace. Mounts vanish on exit.
set -eu
task_repo=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
task_env="$task_repo/compiler/build/openjdk-port/host"
task_workspace=$(dirname -- "$task_repo")
task_cwd=$(pwd -P)
case "$task_cwd" in "$task_workspace"|"$task_workspace"/*) ;; *) task_cwd="$task_repo" ;; esac
test -f "$task_env/usr/bin/python3"
test "$(id -u)" = 0
awk '$1 == 0 && $2 != 0 && $3 == 1 { ok = 1 } END { exit !ok }' /proc/self/uid_map
mount --make-rprivate /
mkdir -p "$task_env$task_workspace" "$task_env/proc" "$task_env/dev" "$task_env/sys"
mount --bind "$task_workspace" "$task_env$task_workspace"
mount -t proc proc "$task_env/proc"
mount --rbind /dev "$task_env/dev"
mount --rbind /sys "$task_env/sys"
exec /usr/sbin/chroot "$task_env" /bin/sh -c 'cd "$1" || exit 1; shift; exec "$@"' \
    sh "$task_cwd" /usr/bin/env PATH=/usr/bin:/bin LC_ALL=C.UTF-8 "$@"
