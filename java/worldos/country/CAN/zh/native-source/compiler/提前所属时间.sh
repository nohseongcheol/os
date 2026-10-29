#!/bin/sh
set -eu
compiler_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec java -XX:-UsePerfData "-Djkoros.compiler.resources=$compiler_root/Java工具" "$compiler_root/Java工具/提前所属时间编译器.java" "$@"
