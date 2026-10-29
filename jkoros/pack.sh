#!/bin/sh
set -eu
# gzip으로 압축한 dist/jkoros-source.tar.gz 배포본을 만든다.
project_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$#" -gt 0 ] && [ "${1#-}" = "$1" ]; then
    output=$1
    shift
    exec python3 "$project_root/distribution/portable.py" pack --root "$project_root" --output "$output" "$@"
fi
exec python3 "$project_root/distribution/portable.py" pack --root "$project_root" "$@"
