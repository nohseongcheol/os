#!/bin/sh
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
set -eu
trap 'echo JKOROS_GUEST_TEST_FAIL; sync; /bin/busybox poweroff -f' EXIT
mkdir -p /mnt/migration
mount -t ext4 /dev/vdc /mnt/migration
test ! -e /mnt/migration/user
# GNU cp preserves ownership, permissions, symlinks, device whiteouts and xattrs.
cp -a /run/jkoros/data/user /mnt/migration/user
/bin/busybox cmp /run/jkoros/data/user/.jkoros/system/base-id /mnt/migration/user/.jkoros/system/base-id
sync
umount /mnt/migration
echo JKOROS_HOME_MIGRATION_PASS
echo JKOROS_GUEST_TEST_PASS
trap - EXIT
/bin/busybox poweroff -f
