#!/bin/sh
set -eu
export PATH=/usr/lib/jvm/java-25-openjdk/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
export JAVA_HOME=/usr/lib/jvm/java-25-openjdk
export LANG=C.UTF-8 LC_ALL=C.UTF-8
fail() { echo JKOROS_GUEST_TEST_FAIL; sync; poweroff; }
trap fail EXIT
stage=seed
for p in $(cat /proc/cmdline); do case "$p" in jkoros.test=*) stage=${p#*=};; esac; done
echo "JKOROS_TEST_STAGE=$stage"
if [ "$stage" = restore ]; then
    test -f /home/user/有效性驗證資料.txt
    test -f /etc/jkoros-migration-check
    test "$(cat /etc/jkoros-migration-check)" = portable-system-change
    test -x /usr/local/bin/portable-user-program
    test "$(portable-user-program)" = portable-program-pass
    test -f /home/user/.local/portable-python/value.txt
    su - user -c '~/.venvs/portable/bin/python -c '\''import portable_demo; assert portable_demo.value == "使用者 安裝值 程式"'\'''
    test ! -e /etc/motd
    test "$(stat -c %u /etc/jkoros-migration-check)" = 0
    if [ -d /opt/jkoros/tests/packages ]; then apk info -e tree; tree --version; fi
    su - user -c '. /etc/profile; ~/workspace/package-test/執行命令'
    test "$(su - user -c 'sudo -n /usr/bin/id -u')" = 0
    echo JKOROS_RESTORE_PASS
else
    uname -m
    java -version
    javac -version
    python3 --version
    gcc --version
    if touch /run/jkoros/system/should-not-write 2>/dev/null; then exit 1; fi
    if [ -x /usr/lib/jvm/java-25-jre/bin/java ]; then /usr/lib/jvm/java-25-jre/bin/java -version; fi
    Xvfb :1 -screen 0 1024x768x24 -nolisten tcp -ac >/var/log/test-xvfb.log 2>&1 &
    n=0
    while [ ! -S /tmp/.X11-unix/X1 ]; do n=$((n+1)); test "$n" -lt 60; sleep 1; done
    su - user -c 'DISPLAY=:1 java -cp /opt/jkoros/tests:/opt/jkoros/lib/中文Java.jar 測試整合 gui'
    su - user -c 'python3 /opt/jkoros/tests/python-test.py'
    gcc -Wall -Werror -pthread /opt/jkoros/tests/thread-test.c -o /tmp/thread-test
    /tmp/thread-test
    su - user -c '. /etc/profile; set -e; mkdir -p ~/workspace/package-test; cd ~/workspace/package-test; jclassc --target openjdk --entry 測試整合 --bundle-runtime /usr/lib/jvm/java-25-jre --classpath /opt/jkoros/lib/中文Java.jar -o 執行命令 /opt/jkoros/tests/測試整合.java; JAVA_HOME=/missing ./執行命令'
    printf 'portable-system-change\n' > /etc/jkoros-migration-check
    printf '#!/bin/sh\necho portable-program-pass\n' > /usr/local/bin/portable-user-program
    chmod 755 /usr/local/bin/portable-user-program
    rm -f /etc/motd
    # Add a package through the actual package manager when an offline package is supplied.
    if [ -d /opt/jkoros/tests/packages ]; then
        apk add --no-network /opt/jkoros/tests/packages/*.apk
        tree --version
    fi
    echo JKOROS_SEED_PASS
fi
sync
trap - EXIT
echo JKOROS_GUEST_TEST_PASS
poweroff
