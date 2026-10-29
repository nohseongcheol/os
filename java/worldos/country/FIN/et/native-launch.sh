#!/bin/sh
set -eu
edition_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec java -XX:-UsePerfData "-Dworldos.edition.root=$edition_root" "$edition_root/native-java/Kantri_käiviti.java" "$@"
