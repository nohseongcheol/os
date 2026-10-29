#!/bin/sh
set -eu
script_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if ! command -v python3 >/dev/null 2>&1; then
    if [ "$(id -u)" -eq 0 ]; then
        apt-get update
        apt-get install -y python3 ca-certificates
    else
        sudo apt-get update
        sudo apt-get install -y python3 ca-certificates
    fi
fi
if [ "${1:-}" = --prepare ]; then
    shift
    exec python3 "$script_root/distribution/portable.py" prepare "$@"
fi
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 ARCHIVE.tar.xz NEW_DIRECTORY [--profile all|native] [--no-host-install]" >&2
    echo "Default: extract, automatically download dependencies and prepare the Ubuntu build environment." >&2
    exit 2
fi
exec python3 - "$@" <<'PY'
import hashlib
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
archive = Path(sys.argv[1]).resolve()
checksum = Path(str(archive) + '.sha256')
if checksum.exists():
    digest = hashlib.sha256()
    with archive.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): digest.update(chunk)
    if digest.hexdigest() != checksum.read_text().split()[0]:
        raise SystemExit('Release archive checksum mismatch')
with tempfile.TemporaryDirectory(prefix='portable-unpack-') as temporary:
    helper = Path(temporary) / 'portable.py'
    with tarfile.open(str(archive)) as stream:
        member = stream.getmember('distribution/portable.py')
        if not member.isfile() or member.size > 1024 * 1024:
            raise SystemExit('Invalid release bootstrap')
        helper.write_bytes(stream.extractfile(member).read())
    result = subprocess.call([sys.executable, str(helper), 'unpack'] + sys.argv[1:])
    sys.exit(result)
PY
