#!/usr/bin/env python3
"""Cross-link and export real precompiled ARM64 JDK/JRE distributions."""
import argparse
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tarfile
from prepare import ROOT, digest


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--existing-jre', action='store_true', help='export already linked build/jre-aarch64')
    args = p.parse_args()
    host = ROOT / 'build/host'
    target = ROOT / 'build/rootfs/usr/lib/jvm/java-25-openjdk'
    jre = ROOT / 'build/jre-aarch64'
    if not args.existing_jre:
        pending = ROOT / 'build/jre-aarch64.next'
        if pending.exists():
            shutil.rmtree(str(pending))
        command = [str(host / 'lib/ld-musl-x86_64.so.1'), '--library-path',
                   str(host / 'usr/lib') + ':' + str(host / 'lib'), str(host / 'usr/bin/proot'),
                   '-R', str(host), '-b', str(ROOT) + ':/work', '-w', '/',
                   '/usr/lib/jvm/java-25-openjdk/bin/jlink', '--module-path',
                   '/work/build/rootfs/usr/lib/jvm/java-25-openjdk/jmods', '--add-modules',
                   'java.se,jdk.charsets,jdk.crypto.ec,jdk.localedata,jdk.zipfs,jdk.unsupported,jdk.httpserver,jdk.management,jdk.naming.dns',
                   '--output', '/work/build/jre-aarch64.next', '--no-header-files', '--no-man-pages']
        subprocess.run(command, check=True)
        if jre.exists():
            shutil.rmtree(str(jre))
        pending.rename(jre)
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    result = []
    for name, tree in [('jdk', target), ('jre', jre)]:
        binary = (tree / 'bin/java').read_bytes()
        if binary[:4] != b'\x7fELF' or struct.unpack_from('<H', binary, 18)[0] != 183:
            raise SystemExit('Runtime is not ARM64: ' + str(tree))
        output = out / ('openjdk25-' + name + '-linux-aarch64-musl.tar.gz')
        def owner(info):
            info.uid = info.gid = 0
            info.uname = info.gname = 'root'
            return info
        with tarfile.open(str(output), 'w:gz') as tar:
            tar.add(str(tree), arcname='openjdk25-' + name, filter=owner)
        result.append({'file': output.name, 'sha256': digest(output), 'bytes': output.stat().st_size,
                       'architecture': 'aarch64', 'libc': 'musl', 'source': 'signed Alpine OpenJDK packages'})
    (out / 'java-runtimes.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
