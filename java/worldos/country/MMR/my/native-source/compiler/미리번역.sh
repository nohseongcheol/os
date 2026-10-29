#!/bin/sh
set -eu
compiler_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec java -XX:-UsePerfData "-Djkoros.compiler.resources=$compiler_root/Javaကိရိယာ" "$compiler_root/Javaကိရိယာ/ကြိုတင်ဘာသာပြန်.java" "$@"
