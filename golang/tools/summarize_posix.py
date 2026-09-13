#!/usr/bin/env python3
"""Match saved guest evidence to the CURRENT native-source build artifacts."""
import csv
import argparse
import json
from pathlib import Path
import re

from install_shells import editions
from native_source import safe, local_path
from posix_build import digest, verify


def rows(path):
    with path.open(encoding='utf-8') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def apply_retry(original, retry):
    """Keep original reports intact; accept only the exact same tested artifacts."""
    indexed = {(row['edition'], row['case']): row for row in original}
    if len(indexed) != len(original):
        raise RuntimeError('Duplicate original test case')
    seen = set()
    for row in retry:
        key = (row['edition'], row['case'])
        if key not in indexed or key in seen:
            raise RuntimeError('Unknown or duplicate retry case: ' + str(key))
        seen.add(key)
        previous = indexed[key]
        if any(previous[field] != row[field] for field in ('program_sha256', 'kernel_iso_sha256')):
            raise RuntimeError('Retry changed executable or kernel: ' + str(key))
        indexed[key] = row
    return list(indexed.values())


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir', type=Path, default=root / 'build-verification/posix')
    parser.add_argument('--retry-dir', type=Path, action='append', default=[],
                        help='retry evidence for unchanged artifacts; original failures stay on disk')
    args = parser.parse_args()
    reports = args.report_dir
    records = editions(root)
    builds = {row['edition']: row for row in rows(reports / 'build-all.tsv')}
    native = rows(reports / 'boot-all.tsv')
    suites = rows(reports / 'boot-selected.tsv')
    initial_failures = [row for row in suites if row['result'] != 'PASS']
    retries = []
    for directory in args.retry_dir:
        retried = rows(directory / 'boot-selected.tsv')
        suites = apply_retry(suites, retried)
        retries.append({'directory': str(directory), 'guest_cases': len(retried)})
    if len(native) != len(records) or {row['edition'] for row in native} != {r[0] for r in records}:
        raise RuntimeError('Missing or duplicate native guest boot results')
    configurations = {}
    for edition, parent, _ in records:
        entry = json.loads((parent / 'posix-entry.json').read_text(encoding='utf-8'))
        package = safe(parent, entry['directory'])
        config = json.loads((package / 'posix.json').read_text(encoding='utf-8'))
        verify(package, config)
        result = builds[edition]
        if result['build'] != 'PASS' or result['manifest_sha256_or_error'] != digest((package / 'posix.json').read_bytes()):
            raise RuntimeError('Build evidence is stale: ' + edition)
        stamp = json.loads((package / 'build/build.json').read_text(encoding='utf-8'))
        if stamp['manifest_sha256'] != result['manifest_sha256_or_error']:
            raise RuntimeError('Build stamp is stale: ' + edition)
        for relative, expected in stamp['inputs'].items():
            if digest(safe(package, relative).read_bytes()) != expected:
                raise RuntimeError('Built input is stale: ' + edition + '/' + relative)
        for filename in ('posix_build.py', 'native_source.py'):
            if (package / filename).read_bytes() != (root / 'tools' / filename).read_bytes():
                raise RuntimeError('Outdated package build helper: ' + edition)
        configurations[edition] = (parent, package, config)
    programs = {'native': 'posix-native-probe', 'library': 'posix-library-runtime', 'core': 'posix-runtime', 'heap': 'posix-heap-runtime',
                'fork': 'posix-fork-runtime', 'exec': 'posix-exec-runtime', 'stdin': 'posix-stdin-runtime', 'socket': 'posix-socket-runtime'}
    for row in native + suites:
        parent, package, _ = configurations[row['edition']]
        if row['result'] != 'PASS' or digest((package / 'build' / programs[row['case']]).read_bytes()) != row['program_sha256']:
            raise RuntimeError('Guest evidence no longer matches executable: ' + str(row))
        if digest(local_path(parent, '소스/build/kernel.iso').read_bytes()) != row['kernel_iso_sha256']:
            raise RuntimeError('Guest evidence no longer matches kernel ISO: ' + row['edition'])
    for edition in {row['edition'] for row in suites}:
        cases = [row['case'] for row in suites if row['edition'] == edition]
        if len(cases) != len(programs) or set(cases) != set(programs):
            raise RuntimeError('Incomplete eight-case regression suite: ' + edition)
    disks = [json.loads((reports / name).read_text()) for name in ('source-disk-all.json', 'source-disk-selected.json')]
    disks += [json.loads((directory / 'source-disk-selected.json').read_text()) for directory in args.retry_dir]
    if any(not item['unchanged'] or item['before'] != item['after'] for item in disks):
        raise RuntimeError('Source disk changed during verification')
    shell_builds = rows(root / 'build-verification/shell-build-status.tsv')
    if len(shell_builds) != len(records) or any(row['shell_idle_probe_elf'] != 'PASS' for row in shell_builds):
        raise RuntimeError('Missing successful shell builds')
    shell_boots = {row['edition']: row for row in rows(root / 'build-verification/shell-boot-status.tsv')}
    selected = sorted({row['edition'] for row in suites})
    for edition in selected:
        parent, _, _ = configurations[edition]
        entry = json.loads((parent / 'shell-entry.json').read_text(encoding='utf-8'))
        package = safe(parent, entry['directory'])
        result = shell_boots[edition]
        if result['result'] != 'PASS' or result['shell_elf_sha256'] != digest((package / 'build/worldos-shell').read_bytes()):
            raise RuntimeError('Shell boot evidence is stale: ' + edition)
        if result['kernel_elf_sha256'] != digest(local_path(parent, '소스/build/kernel.bin').read_bytes()):
            raise RuntimeError('Shell kernel evidence is stale: ' + edition)
    tests = (reports / 'unit-tests.log').read_text(encoding='utf-8')
    tested = re.search(r'Ran (\d+) tests', tests)
    if not tested or not tests.rstrip().endswith('OK'):
        raise RuntimeError('No successful unit-test record')
    summaries = [config['summary'] for _, _, config in configurations.values()]
    report = {'editions': len(records), 'current_builds_verified': len(builds),
        'native_guest_boots': len(native), 'current_artifacts_match_saved_boots': True,
        'regression_guest_cases': len(suites), 'regression_editions': sorted({row['edition'] for row in suites}),
        'initial_regression_failures': initial_failures, 'unchanged_artifact_retries': retries,
        'unit_tests_passed': int(tested.group(1)),
        'shell_builds_passed': len(shell_builds), 'current_shell_boots_verified': selected,
        'functions_per_edition': sorted(set(s['functions'] for s in summaries)),
        'selected_identifiers_per_edition': sorted(set(s['variables'] for s in summaries)),
        'all_function_names_present': sum(s['named_functions'] == s['functions'] for s in summaries),
        'english_editions_in_that_count': sum(s['language'] == 'en' for s in summaries),
        'partial_or_undefined_language_editions': sum(s['named_functions'] != s['functions'] for s in summaries),
        'all_selected_variable_names_present': sum(s['named_variables'] == s['variables'] for s in summaries),
        'complete_POSIX_implementation': False,
        'implementation_scope': 'i386; single-thread; C-locale; kernel-dependent file/socket support',
        'linguistic_review': 'incomplete', 'complete_translation_all_identifiers': False,
        'source_disks_unchanged': True}
    (reports / 'delivery-summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
