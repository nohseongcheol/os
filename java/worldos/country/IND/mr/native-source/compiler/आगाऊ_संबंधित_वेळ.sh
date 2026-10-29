#!/bin/sh
set -eu
compiler_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec java -XX:-UsePerfData "-Djkoros.compiler.resources=$compiler_root/जावा_साधने" "$compiler_root/जावा_साधने/आगाऊ_संबंधित_वेळ_संकलक.java" "$@"
