#!/usr/bin/env python3
"""Compile named optional packages not linked into the primary kernel."""
import csv
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import subprocess
from native_source import local_path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ['src/amd_am79c973/amd_am79c973.go', 'src/etherframe/etherframe.go',
            'src/arp/arp.go', 'src/ipv4/ipv4.go', 'src/icmp/icmp.go', 'src/udp/udp.go',
            'src/util/array/array.go', 'src/vga/vga.go', 'src/widget/widget.go',
            'src/drivers/timer/timer.go']


def check(code):
    tree = local_path(ROOT / '나라' / code, '소스')
    with local_path(tree, '파일대응표.tsv').open(encoding='utf-8') as stream:
        mapped = dict(list(csv.reader(stream, delimiter='\t'))[1:])
    packages = [str(Path(mapped[name]).parent)[4:] for name in PACKAGES]
    result = subprocess.run(['go', 'build'] + packages, cwd=str(tree),
                            env=dict(os.environ, GOARCH='386', GOPATH=str(tree)),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (ROOT / 'build-verification' / (code + '-packages.log')).write_bytes(result.stdout)
    return code, 'PASS' if result.returncode == 0 else 'FAIL'


def main():
    codes = sorted(p.name for p in (ROOT / '나라').iterdir() if p.is_dir())
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(check, codes))
    with (ROOT / 'build-verification/named-packages-status.tsv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(['country', 'result'])
        writer.writerows(results)
    failures = [code for code, result in results if result != 'PASS']
    print('optional package checks: {} countries, {} failed'.format(len(codes), len(failures)))
    if failures:
        raise SystemExit('failed: ' + ', '.join(failures))


if __name__ == '__main__':
    main()
