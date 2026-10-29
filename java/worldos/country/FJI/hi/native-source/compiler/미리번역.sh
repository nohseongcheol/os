#!/bin/sh
set -eu
compiler_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec java -XX:-UsePerfData "-Djkoros.compiler.resources=$compiler_root/जावासाधन" "$compiler_root/जावासाधन/पूर्वसंकलक.java" "$@"
