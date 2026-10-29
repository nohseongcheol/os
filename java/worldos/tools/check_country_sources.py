#!/usr/bin/env python3
"""Compile all first-party Java layers and check native input/C/Python sources."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'native'))
import verify
from generate import translate
from country_naming import names_for_country
from verify_country_boots import source_digest


def check(item):
    language, (folder, config) = item
    source_hash = source_digest(folder, config)
    result = verify.check_language((folder, config))
    result.update(edition=str(folder.relative_to(ROOT)), source_sha256=source_hash)
    if not result['passed']:
        return result
    source, mapping = folder / config['source'], config['identifiers']
    def local(name):
        return source / translate(name, mapping)
    # check_language already compiled the host tools, ARM64 kernel, user JVM,
    # native library and examples. Compile the remaining layers once.
    extra = (list(local('원천').rglob('*.java')) +
             list(local('한국어자바/원문').rglob('*.java')) +
             list(local('os/원문').glob('*.java')))
    try:
        with tempfile.TemporaryDirectory(prefix='worldos-extra-java-') as destination:
            subprocess.check_output(['javac', '-J-XX:-UsePerfData', '--release', '11',
                                     '-encoding', 'UTF-8', '-d', destination] + [str(p) for p in extra],
                                    stderr=subprocess.STDOUT)
        result['managed_and_x86_java_compiled'] = True
        if source_digest(folder, config) != source_hash:
            raise ValueError('Source changed during compilation')
    except subprocess.CalledProcessError as error:
        result['passed'] = False
        result['error'] = error.output.decode('utf-8', 'replace')
        print(result['error'], flush=True)
    except ValueError as error:
        result.update(passed=False, error=str(error))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--languages', nargs='+', required=True)
    parser.add_argument('--countries', nargs='+', help='Limit representatives to these countries')
    args = parser.parse_args()
    verify.OUT = ROOT / 'build/country-localization/compilation'
    verify.OUT.mkdir(parents=True, exist_ok=True)
    representatives = {}
    for path in sorted((ROOT / 'country').glob('*/native.json')) + sorted((ROOT / 'country').glob('*/*/native.json')):
        config = json.loads(path.read_text())
        if (config['language'] in args.languages and config['identifiers'] == names_for_country(config['country'], config['language']) and
                (not args.countries or config['country'] in args.countries)):
            representatives.setdefault(config['language'], (path.parent, config))
    missing = set(args.languages) - set(representatives)
    if missing:
        parser.error('No edition with the current names: ' + ','.join(sorted(missing)))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(check, representatives.items()))
    report = {'passed': all(r['passed'] for r in results), 'results': results}
    target = verify.OUT / ('check-' + '-'.join(sorted(args.languages)) + '.json')
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
