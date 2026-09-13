#!/usr/bin/env python3
"""Force representative parent Makefile -> localized kernel -> ISO builds."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess

from generate_script_variants import table
from install_shells import editions
from native_source import local_path
from posix_build import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', action='append', default=[])
    args = parser.parse_args()
    selected = args.edition or ['KOR', 'CHN', 'USA', 'JPN', 'FRA', 'DEU', 'CHN/zh_Hans', 'CHN/zh_Hant',
                               'JPN/ja_Hira', 'JPN/ja_Kana', 'IND/hi_Deva', 'IND/ta_Taml', 'SRB/sr_Cyrl']
    records = {record[0]: record for record in editions(args.root)}
    if set(selected) - set(records):
        parser.error('Unknown edition')
    reports = args.root / 'build-verification/layout'
    reports.mkdir(parents=True, exist_ok=True)
    def check(edition):
        parent = records[edition][1]
        kernel = local_path(parent, '소스')
        with (reports / (edition.replace('/', '-') + '.kernel.log')).open('wb') as output:
            result = subprocess.run(['make', '-B', '-C', str(parent), 'source-iso'], stdout=output, stderr=subprocess.STDOUT)
        passed = result.returncode == 0 and (kernel / 'build/kernel.iso').is_file()
        print(edition, 'kernel+ISO', 'PASS' if passed else 'FAIL', flush=True)
        return [edition, 'PASS' if passed else 'FAIL', str(kernel.relative_to(args.root)),
                digest((kernel / 'build/kernel.iso').read_bytes()) if passed else '']
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(check, selected))
    (reports / 'kernel-builds.tsv').write_text(table(['edition', 'result', 'source_path', 'kernel_iso_sha256'], results), encoding='utf-8')
    raise SystemExit(0 if all(row[1] == 'PASS' for row in results) else 1)


if __name__ == '__main__':
    main()
