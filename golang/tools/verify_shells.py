#!/usr/bin/env python3
"""Verify all installed shell editions and optionally compile freestanding ELF."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import json
from pathlib import Path
import subprocess

from install_shells import editions
from generate_script_variants import table
from shell_build import verify
from native_source import safe


def check(root, record, build):
    edition, parent, language = record
    entry = json.loads((parent / 'shell-entry.json').read_text(encoding='utf-8'))
    directory = safe(parent, entry['directory'])
    config = json.loads((directory / 'shell.json').read_text(encoding='utf-8'))
    verify(directory, config)
    result = [edition, language, 'PASS', 'NOT_RUN', config['canonical_sha256']]
    if build:
        logs = root / 'build-verification/shells'
        logs.mkdir(parents=True, exist_ok=True)
        with (logs / (edition.replace('/', '-') + '.log')).open('wb') as log:
            process = subprocess.run(['make', '-C', str(directory)], stdout=log, stderr=subprocess.STDOUT)
        result[3] = 'PASS' if process.returncode == 0 else 'FAIL'
        if process.returncode == 0:
            for artifact in ('worldos-shell', 'worldos-idle', 'worldos-shell-probe'):
                header = (directory / 'build' / artifact).read_bytes()[:20]
                if header[:7] != b'\x7fELF\x01\x01\x01' or header[16:20] != b'\x02\x00\x03\x00':
                    result[3] = 'FAIL'
    print(edition, *result[2:4], flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', action='append', default=[])
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    records = editions(args.root)
    if set(args.edition) - {row[0] for row in records}:
        parser.error('unknown shell edition')
    records = [row for row in records if not args.edition or row[0] in args.edition]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda record: check(args.root, record, args.build), records))
    report = args.root / 'build-verification/shell-build-status.tsv'
    report.parent.mkdir(exist_ok=True)
    previous = {}
    if report.exists():
        with report.open(encoding='utf-8') as stream:
            previous = {row[0]: row for row in list(csv.reader(stream, delimiter='\t'))[1:]}
    for result in results:
        old = previous.get(result[0])
        if old and not args.build and old[-1] == result[-1]:
            result[3] = old[3]
        previous[result[0]] = result
    report.write_text(table(['edition', 'language', 'source_and_lowering', 'shell_idle_probe_elf', 'canonical_sha256'], sorted(previous.values())), encoding='utf-8')
    if any('FAIL' in row for row in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
