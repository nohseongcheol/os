#!/bin/sh
set -eu
compiler_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec java -XX:-UsePerfData "-Djkoros.compiler.resources=$compiler_root/OutilJava" "$compiler_root/OutilJava/CompilationAnticipée.java" "$@"
