#!/bin/sh
set -eu
export PATH=/usr/lib/jvm/java-25-openjdk/bin:/usr/bin:/bin:/usr/sbin:/sbin
export DISPLAY=:0
mkdir -p /home/user/workspace/test-classes
chown -R user:user /home/user/workspace
su user -c 'dbus-run-session /opt/worldos/run-user-tests.sh'
