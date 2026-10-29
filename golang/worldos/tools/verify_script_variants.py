#!/usr/bin/env python3
"""Check independent sources and exact lowering; optionally build every edition."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from generate_script_variants import profiles, table
from native_source import stage, verify, local_path


def check(root, record, build):
    country, profile = record[:2]
    tree = local_path(root / '문자판' / country / profile, '소스')
    manifest = json.loads(local_path(tree, '문자대응.json').read_text(encoding='utf-8'))
    verify(tree, manifest)
    with tempfile.TemporaryDirectory(prefix='variant-check-') as temporary:
        destination = Path(temporary)
        stage(tree, destination, manifest)
        for entry in manifest['files']:
            restored = (destination / entry['compiler']).read_bytes()
            if hashlib.sha256(restored).hexdigest() != entry['compiler_sha256']:
                raise RuntimeError('Non-lossless lowering: ' + profile + '/' + entry['compiler'])
    results = [country, profile, 'PASS', 'NOT_RUN', 'NOT_RUN']
    if build:
        logs = root / 'build-verification/script-variants'
        logs.mkdir(parents=True, exist_ok=True)
        for index, target in [(3, 'iso'), (4, 'userland')]:
            with (logs / (country + '-' + profile + '-' + target + '.log')).open('wb') as output:
                process = subprocess.run(['make', '-C', str(tree), target], stdout=output, stderr=subprocess.STDOUT)
            results[index] = 'PASS' if process.returncode == 0 else 'FAIL'
    print(country, profile, *results[2:], flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--profile', action='append', default=[])
    args = parser.parse_args()
    selected = [record for record in profiles() if not args.profile or record[1] in args.profile]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda record: check(args.root, record, args.build), selected))
    report = args.root / 'build-verification/script-variant-status.tsv'
    report.parent.mkdir(exist_ok=True)
    # Read-only verification must not erase earlier successful build evidence.
    previous = {}
    if report.exists():
        with report.open(encoding='utf-8') as stream:
            previous = {tuple(row[:2]): row for row in list(csv.reader(stream, delimiter='\t'))[1:]}
    for result in results:
        old = previous.get(tuple(result[:2]))
        if old and not args.build:
            result[3:] = old[3:]
        previous[tuple(result[:2])] = result
    report.write_text(table(['country', 'profile', 'source_roundtrip', 'kernel_iso', 'posix_tests_build'], sorted(previous.values())), encoding='utf-8')
    if any('FAIL' in result for result in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
