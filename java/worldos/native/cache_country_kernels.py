#!/usr/bin/env python3
"""Prepare independent image copies for exactly equal, verified source trees.

This feeds the running per-country boot verifier; it does not replace boot
tests. No source links or borrowed-language images are used. Differing owned
source bytes, filenames, or dependency archives require a separate build.
"""
import hashlib
import json
from pathlib import Path
import shutil
import time
from verify_country_boots import ROOT, source_digest, digest


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + '.new')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def main():
    output = ROOT / 'build/native/country-boots'
    cache = output / 'equal-source-kernels'
    cache.mkdir(parents=True, exist_ok=True)
    folders = sorted(p.parent for p in (ROOT / 'country').glob('*/native.json'))
    kernels = {}
    imported = set()
    prepared = []
    deadline = time.monotonic() + 12*3600
    while time.monotonic() < deadline:
        try:
            summary = json.loads((output / 'summary.json').read_text())
        except (OSError, ValueError):
            time.sleep(2)
            continue
        for report in summary['results']:
            identity = (report['country'], report.get('source_sha256'), report.get('kernel_sha256'))
            if identity in imported or not report.get('passed'):
                continue
            folder = ROOT / report['edition']
            try:
                config = json.loads((folder / 'native.json').read_text())
                kernel = folder / config['source'] / config['native'] / 'build/kernel8.img'
                if source_digest(folder, config) != report['source_sha256'] or digest(kernel) != report['kernel_sha256']:
                    continue
                key = (report['source_sha256'], config['vendor_sha256'])
                if key not in kernels:
                    cached = cache / (report['source_sha256'] + '.img')
                    shutil.copyfile(str(kernel), str(cached))
                    assert digest(cached) == report['kernel_sha256']
                    evidence = {'source_sha256': report['source_sha256'],
                                'kernel_sha256': report['kernel_sha256'],
                                'vendor_sha256': config['vendor_sha256'],
                                'origin_country': report['country'],
                                'origin_report': str((output / report['country'] / 'report.json').relative_to(ROOT)),
                                'scope': 'All owned filenames and source bytes equal. Independent image copy; this target still requires its own actual boot test.'}
                    atomic_json(cached.with_suffix('.json'), evidence)
                    kernels[key] = (cached, evidence)
                imported.add(identity)
            except (OSError, ValueError):
                continue
        # Stay well ahead of the two ordered workers. Never touch an existing
        # build, a completed test, or a country near either active worker.
        checked = {r['country'] for r in summary['results']}
        frontier = max((i for i, f in enumerate(folders) if f.name in checked), default=-1)
        for index, folder in enumerate(folders):
            if folder.name in checked or index <= frontier + 20:
                continue
            try:
                config = json.loads((folder / 'native.json').read_text())
                build = folder / config['source'] / config['native'] / 'build'
                if build.exists():
                    continue
                source_hash = source_digest(folder, config)
                value = kernels.get((source_hash, config['vendor_sha256']))
                if value is None:
                    continue
                cached, evidence = value
                # mkdir without exist_ok also protects a build started since
                # the initial check. Existing build outputs are never replaced.
                build.mkdir()
                temporary = build / 'kernel8.img.new'
                shutil.copyfile(str(cached), str(temporary))
                assert digest(temporary) == evidence['kernel_sha256']
                temporary.replace(build / 'kernel8.img')
                atomic_json(build / 'worldos-kernel-cache.json', evidence)
                marker = build / 'worldos-source.sha256.new'
                marker.write_text(source_hash + '\n')
                marker.replace(build / 'worldos-source.sha256')
                prepared.append({'country': folder.name, **evidence})
                atomic_json(output / 'equal-source-cache.json', {'prepared': prepared})
                print('PREPARED', folder.name, 'from', evidence['origin_country'], flush=True)
            except (OSError, ValueError):
                continue
        if summary.get('complete'):
            break
        time.sleep(5)


if __name__ == '__main__':
    main()
