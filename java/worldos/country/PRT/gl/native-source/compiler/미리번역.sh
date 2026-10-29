#!/bin/sh
set -eu
compiler_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec java -XX:-UsePerfData "-Djkoros.compiler.resources=$compiler_root/자바도구" "$compiler_root/자바도구/기계어미리번역.java" "$@"
