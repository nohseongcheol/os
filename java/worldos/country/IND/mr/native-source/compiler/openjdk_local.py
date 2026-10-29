#!/usr/bin/env python3
"""Use this workspace's isolated Linux build environment (does not install packages)."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proot', action='store_true', help='Slower fallback when user/mount namespaces are unavailable')
    parser.add_argument('action', choices=('build', 'test', 'java', 'javac'))
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    work = root / 'compiler/build/openjdk-port'
    host = root / 'platforms/rpi4/build/host'
    image = work / 'linux-x86_64/images/jdk'
    required = [work / 'host/usr/bin/python3']
    if args.proot: required += [host / 'lib/ld-musl-x86_64.so.1', host / 'usr/bin/proot']
    for p in required:
        if not p.exists(): parser.error('Prepared local environment missing: ' + str(p))
    if args.action == 'build':
        if args.arguments: parser.error('build uses the pinned workspace configuration; use openjdk_build.py for options')
        record = json.loads((work / 'source.json').read_text())
        target = ['/usr/bin/python3', str(root / 'compiler/संकलक.py'), '--target', 'openjdk-build',
                  '--java-home', '/usr/lib/jvm/java-25-openjdk', '--jobs', '2',
                  '-o', str(work / 'linux-x86_64'), record['source_directory']]
    elif args.action == 'test':
        target = ['/usr/bin/python3', str(root / 'compiler/test_openjdk_image.py'),
                  '--jdk', str(image), '--output', str(work / 'smoke')] + args.arguments
    else:
        if not (image / 'bin' / args.action).is_file(): parser.error('Build the OpenJDK image first')
        target = [str(image / 'bin' / args.action)] + args.arguments
    if args.proot:
        cwd = Path.cwd().resolve()
        if cwd != root.parent and root.parent not in cwd.parents: cwd = root
        cmd = [str(host / 'lib/ld-musl-x86_64.so.1'), '--library-path', str(host / 'usr/lib') + ':' + str(host / 'lib'),
               str(host / 'usr/bin/proot'), '-r', str(work / 'host'), '-b', '/dev', '-b', '/proc', '-b', '/sys',
               '-b', str(root.parent), '-w', str(cwd), '/usr/bin/env', 'PATH=/usr/bin:/bin', 'LC_ALL=C.UTF-8'] + target
    else:
        cmd = ['unshare', '--user', '--map-root-user', '--mount', '--pid', '--fork',
               'bash', str(root / 'compiler/openjdk_namespace.sh')] + target
    return subprocess.call(cmd)


if __name__ == '__main__': sys.exit(main())
