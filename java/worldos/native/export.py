#!/usr/bin/env python3
"""Export a native country with real archive files for independent use."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
from archives import ARCHIVES, ROOT, sha256


def export_country(original, destination):
    original, destination = Path(original).resolve(), Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Export destination already exists: ' + str(destination))
    manifest = json.loads((original / 'native-generated.json').read_text(encoding='utf-8'))
    config = json.loads((original / 'native.json').read_text(encoding='utf-8'))
    files = dict(manifest)
    files['native-generated.json'] = sha256(original / 'native-generated.json')
    for name, key in ARCHIVES.items():
        files[name] = config[key]
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.native-export-', dir=str(destination.parent)) as temporary:
        staged = Path(temporary) / 'country'
        staged.mkdir()
        for name, expected in files.items():
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Invalid export path: ' + name)
            source = original / relative
            if name not in ARCHIVES and original not in source.resolve().parents:
                raise ValueError('Source is outside the country: ' + name)
            target = staged / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            # Copy bytes so the export owns independent archive files.
            shutil.copy2(str(source), str(target), follow_symlinks=True)
            if sha256(target) != expected:
                raise ValueError('Export checksum mismatch: ' + name)
        if (original / config['source'] / 'ip.conf').is_file():
            # Freeze the effective shared/override settings for offline use.
            import importlib.util
            spec = importlib.util.spec_from_file_location('export_ip_config', ROOT/'tools/ip_config.py')
            helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
            network = helper.read_config(original / config['source'])
            (staged/'ip.conf').write_text(''.join(key+'='+network[key]+'\n' for key in ('IP','NETMASK','GATEWAY','DNS')))
            manifest['ip.conf'] = sha256(staged/'ip.conf')
            (staged/'native-generated.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        example = Path(config['source']) / 'example'
        if example.is_absolute() or '..' in example.parts:
            raise ValueError('Invalid example path: ' + str(example))
        (staged / 'example').symlink_to(str(example), target_is_directory=True)
        if destination.exists() or destination.is_symlink():
            raise FileExistsError('Export destination already exists: ' + str(destination))
        staged.rename(destination)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('country')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if not args.output:
        parser.error('--output must name a new directory')
    if len(args.country) != 3 or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in args.country):
        parser.error('country must be a three-letter code, for example KOR')
    print(export_country(ROOT / 'country' / args.country, Path(args.output)))


if __name__ == '__main__':
    main()
