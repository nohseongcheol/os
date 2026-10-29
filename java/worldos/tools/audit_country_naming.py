#!/usr/bin/env python3
"""Audit territory/language selection and first-party native naming coverage."""
import csv
import argparse
from concurrent.futures import ThreadPoolExecutor
import ast
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import stat
import tokenize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'native'))
from country_naming import country_policy, validate_edition, names_for_country
from terms import names
from generate import identifiers, translator
from source_names import rename_legal_paths

expected_names = names_for_country


@lru_cache(maxsize=4096)
def untranslated(name, data):
    try:
        return {t for t in identifiers(name, data.decode('utf-8'))
                if any('\uac00' <= c <= '\ud7a3' for c in t)}
    except UnicodeDecodeError:
        return set()


@lru_cache(maxsize=4096)
def embedded_untranslated(name, data):
    """Include compiler/fixture source emitted from Python string literals."""
    if not name.endswith('.py'):
        return set()
    result = set()
    for token in tokenize.generate_tokens(io.StringIO(data.decode('utf-8')).readline):
        if token.type != tokenize.STRING:
            continue
        try:
            value = ast.literal_eval(token.string)
        except (ValueError, SyntaxError):
            continue
        if not isinstance(value, str):
            continue
        extension = ('java' if 'class ' in value and '{' in value else
                     'py' if 'def ' in value else 'c' if 'typedef ' in value else None)
        if extension:
            result.update(t for t in identifiers('fixture.' + extension, value)
                          if any('\uac00' <= c <= '\ud7a3' for c in t))
    return result


def check_java(path, data, expected):
    assert hashlib.sha256(data).hexdigest() == expected, 'Java ownership mismatch: ' + str(path)
    match = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', data.decode('utf-8'))
    assert not match or match.group(1) == path.stem, 'Class/file mismatch: ' + str(path)


def check_edition(config_path, legal):
    folder = config_path.parent
    checked, java_checked = 0, 0
    try:
        config = json.loads(config_path.read_text())
        expected = validate_edition(folder, config)
        assert config.get('country_naming') == expected, 'Missing or stale country policy'
        assert config['identifiers'] == expected_names(config['country'], config['language']), 'Stale country/language dictionary'
        rename = translator(tuple(config['identifiers'].items()))
        managed = rename('원천') + '/'
        namespace = expected['namespace']['identifier'] + '.' + expected['namespace']['os_name']
        manifest = json.loads((folder / 'native-generated.json').read_text())
        entry = (folder / 'native-launch.sh').read_text()
        launchers = re.findall(r'''native-java/[^/\s"']+\.java''', entry)
        assert len(launchers)==1 and (folder/launchers[0]).is_file(), 'Missing launcher entry reference'
        for name in ('native.json', 'native-names.tsv', 'native-pending.tsv', 'native-term-evidence.json'):
            assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == manifest[name], name
        for field in ('builder', 'runner', 'image_builder', 'system_tester'):
            if field in config:
                assert (folder / config['source'] / config['native'] / config[field]).is_file(), field
        remaining, embedded, remaining_paths, owned = set(), set(), set(), set()
        for relative in config['owned_files']:
            name = config['source'] + '/' + relative
            owned.add(name)
            path = folder / name
            info = path.lstat()
            assert stat.S_ISREG(info.st_mode) and info.st_nlink == 1, relative
            checked += 1
            data = None
            if relative.endswith('.java') or config['language'] != 'ko':
                data = path.read_bytes()
                assert hashlib.sha256(data).hexdigest() == manifest[name], 'Source ownership mismatch: ' + name
            if relative.endswith('.java'):
                check_java(path, data, manifest[name])
                if relative.startswith(managed):
                    package = re.search(r'^package\s+([^;]+);', data.decode('utf-8'), re.M)
                    expected_package = str(Path(relative[len(managed):]).parent).replace('/', '.')
                    assert package and package.group(1) == expected_package, 'Package/path mismatch: ' + relative
                    assert expected_package.startswith(namespace+'.'), 'Wrong country namespace: ' + relative
                    assert b'"jkoros"' not in data, 'Stale managed system identity: ' + relative
                java_checked += 1
            if config['language'] != 'ko':
                if any('\uac00' <= c <= '\ud7a3' for c in relative):
                    remaining_paths.add(relative)
                remaining.update(untranslated(relative, data))
                embedded.update(embedded_untranslated(relative, data))
        # The outer Java launcher is owned alongside, rather than inside, source.
        for name, digest in manifest.items():
            if name.endswith('.java') and name not in owned:
                path = folder / name
                info = path.lstat()
                assert stat.S_ISREG(info.st_mode) and info.st_nlink == 1, name
                check_java(path, path.read_bytes(), digest)
                if config['language'] != 'ko':
                    remaining.update(untranslated(name, path.read_bytes()))
                    if any('\uac00' <= c <= '\ud7a3' for c in name):
                        remaining_paths.add(name)
                java_checked += 1
            elif name not in owned and name not in ('native.json','native-names.tsv','native-pending.tsv','native-term-evidence.json'):
                path = folder/name
                info = path.lstat()
                assert stat.S_ISREG(info.st_mode) and info.st_nlink==1, name
                assert hashlib.sha256(path.read_bytes()).hexdigest()==digest, 'Outer ownership mismatch: '+name
        for original, text in legal.items():
            relative = rename(original)
            if relative in config['owned_files']:
                assert (folder / config['source'] / relative).read_text() == rename_legal_paths(text, rename), 'Legal prose changed: ' + relative
        with (folder / 'native-pending.tsv').open() as stream:
            pending_rows = list(csv.DictReader(stream, delimiter='\t'))
        assert len(pending_rows) == config['naming']['untranslated_identifiers'], 'Pending list/count mismatch'
        if config['language'] == 'ko':
            assert not pending_rows, 'Korean identifiers are native in a Korean edition'
        if config['language'] != 'ko' and not pending_rows:
            assert not (remaining or embedded or remaining_paths), 'Incomplete supposedly localized edition: ' + ','.join(sorted(remaining | embedded | remaining_paths)[:15])
        row = {'path': str(folder.relative_to(ROOT)), 'country': config['country'],
               'language': config['language'], 'remaining_identifiers': len(pending_rows),
               'remaining_paths': len(remaining_paths), 'remaining_code_identifiers': len(remaining),
               'remaining_embedded_identifiers': len(embedded),
               'native_review': 'pending', 'etymology_review': 'partial'}
        return row, None, checked, java_checked
    except (AssertionError, KeyError, OSError, ValueError) as error:
        return None, {'path': str(folder.relative_to(ROOT)), 'error': str(error)}, checked, java_checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4, choices=range(1, 33), help='Concurrent independent edition reads')
    parser.add_argument('--countries', nargs='+')
    parser.add_argument('--languages', nargs='+')
    parser.add_argument('--require-complete', action='store_true', help='Fail if any selected language still has untranslated names')
    args = parser.parse_args()
    destination = ROOT / 'build/country-localization'
    destination.mkdir(parents=True, exist_ok=True)
    countries, editions, errors, checked, java_checked = country_policy(), [], [], 0, 0
    legal = json.loads((ROOT / 'native/inputs/legal-sources.json').read_text())['files']
    paths = sorted((ROOT / 'country').glob('*/native.json')) + sorted((ROOT / 'country').glob('*/*/native.json'))
    paths = [p for p in paths if (not args.countries or p.relative_to(ROOT / 'country').parts[0] in args.countries)
             and (not args.languages or json.loads(p.read_text())['language'] in args.languages)]
    # Keep identical source vocabularies together so the bounded token-analysis
    # cache can be reused. Every edition's own files and hashes are still read.
    def dictionary_key(path):
        config = json.loads(path.read_text())
        mapping = config['identifiers']
        return config['language'], hashlib.sha256(json.dumps(mapping, sort_keys=True).encode()).hexdigest()
    paths.sort(key=dictionary_key)
    # Each edition owns separate files. Parallel reads avoid a long serial wait
    # on distribution-sized trees; report and status writes stay on this thread.
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        for index, (row, error, count, java_count) in enumerate(executor.map(lambda path: check_edition(path, legal), paths), 1):
            checked += count
            java_checked += java_count
            if row:
                editions.append(row)
            if error:
                errors.append(error)
            if index % 100 == 0:
                print('Checked', index, 'editions', flush=True)
    incomplete = [r['path'] for r in editions if r['remaining_identifiers'] or r['remaining_paths'] or r['remaining_code_identifiers'] or r['remaining_embedded_identifiers']]
    report = {'scope': 'Native owned sources and native Java launchers; hosted Linux edition templates and distribution tools still contain project-owned English identifiers.',
              'passed': not errors and (not args.require_complete or not incomplete), 'countries': len({r['country'] for r in editions}),
              'editions': len(editions), 'independent_source_files_checked': checked,
              'native_java_files_verified': java_checked,
              'english_editions_without_korean_identifiers': sum(r['language'] == 'en' and r['remaining_identifiers'] == 0 for r in editions),
              'editions_with_remaining_translation': sum(r['remaining_identifiers'] > 0 for r in editions),
              'native_speaker_review_complete': False, 'all_etymologies_verified': False,
              'all_names_localized': not errors and not incomplete, 'incomplete_editions': incomplete,
              'legal_clauses_preserved': not errors,
              'editions_detail': editions, 'errors': errors}
    (destination / 'country-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'naming/country-language-policy.json').write_text(json.dumps({
        'territory_source': 'ISO 3166-1 (naming/countries.json)',
        'language_source': 'Unicode CLDR 48; script-specific representatives are explicit project selections',
        'language_reference': 'https://www.unicode.org/cldr/charts/48/supplemental/territory_language_information.html',
        'anguilla_reference': 'https://www.gov.ai/stats/abstract00.htm',
        'countries': countries}, ensure_ascii=False, indent=2) + '\n')
    # Refresh coverage counts only. Existing boot reports keep their original
    # kernel hashes and are never promoted to evidence for a renamed build.
    status = ROOT / 'native/국가별현황.md'
    lines = []
    for line in status.read_text().splitlines():
        match = re.match(r'\| \[([A-Z]{3})\]', line)
        if match:
            code = match.group(1)
            config = json.loads((ROOT / 'country' / code / 'native.json').read_text())
            columns = line.split('|')
            columns[4] = ' ' + str(config['naming']['mapped_identifiers']) + ' '
            columns[5] = ' [{}](../country/{}/native-pending.tsv) '.format(config['naming']['untranslated_identifiers'], code)
            line = '|'.join(columns)
        lines.append(line)
    status.write_text('\n'.join(lines) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('editions_detail',)}, ensure_ascii=False, indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
