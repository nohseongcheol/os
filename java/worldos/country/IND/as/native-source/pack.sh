#!/bin/sh
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$#" -gt 0 ] && [ "${1#-}" = "$1" ]; then
    output=$1
    shift
    exec python3 "$project_root/distribution/portable.py" pack --root "$project_root" --output "$output" "$@"
fi
exec python3 "$project_root/distribution/portable.py" pack --root "$project_root" "$@"
