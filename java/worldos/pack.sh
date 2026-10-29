#!/bin/sh
set -eu
# gzip으로 압축한 dist/worldos-source.tar.gz 배포본을 만든다.
project_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# Older trees used shared archive links. Verify and materialize every country
# before creating a release so each source folder is independently usable.
python3 "$project_root/native/archives.py" materialize
if [ "$#" -gt 0 ] && [ "${1#-}" = "$1" ]; then
    output=$1
    shift
    exec python3 "$project_root/distribution/portable.py" pack --root "$project_root" --output "$output" "$@"
fi
exec python3 "$project_root/distribution/portable.py" pack --root "$project_root" "$@"
