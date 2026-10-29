#!/bin/sh
set -eu
trap 'cp /tmp/fcitx.log /home/user/workspace/fcitx-test.log' 0
. /opt/worldos/input-session.sh
cp /tmp/fcitx.log /home/user/workspace/fcitx-test.log
openbox >/home/user/workspace/openbox-test.log 2>&1 &
sleep 2
javac -encoding UTF-8 -d /home/user/workspace/test-classes /opt/worldos/FontFeatures.java
java -cp /home/user/workspace/test-classes FontFeatures
javac -encoding UTF-8 -d /home/user/workspace/test-classes /opt/worldos/JavaFeatures.java
java -cp /home/user/workspace/test-classes JavaFeatures
javac -encoding UTF-8 -d /home/user/workspace/test-classes /opt/worldos/WorkbenchFeatures.java
java -cp /home/user/workspace/test-classes WorkbenchFeatures
gcc -Wall -Wextra -Werror -Wno-normalized -pthread /opt/worldos/posix.c -o /home/user/workspace/posix-test
/home/user/workspace/posix-test
gcc -Wall -Wextra -Werror -Wno-normalized /opt/worldos/posix-local-test.c -o /home/user/workspace/local-posix-test
/home/user/workspace/local-posix-test
javac -encoding UTF-8 -h /home/user/workspace/test-classes -d /home/user/workspace/test-classes /opt/worldos/NativeBridge.java
gcc -Wall -Wextra -Werror -Wno-normalized -shared -fPIC -I/usr/lib/jvm/java-25-openjdk/include -I/usr/lib/jvm/java-25-openjdk/include/linux -I/home/user/workspace/test-classes /opt/worldos/native_bridge.c -o /home/user/workspace/test-classes/libworldos_jni.so
java --enable-native-access=ALL-UNNAMED -Djava.library.path=/home/user/workspace/test-classes -cp /home/user/workspace/test-classes NativeBridge
javac -encoding UTF-8 -d /home/user/workspace/test-classes /opt/worldos/InputFeatures.java
java -cp /home/user/workspace/test-classes InputFeatures
printf 'WORLDOS_FEATURE_TESTS_OK\n'
