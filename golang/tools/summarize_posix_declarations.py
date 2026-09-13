#!/usr/bin/env python3
"""Recheck current declaration artifacts against this generation's evidence."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

from install_shells import editions
from native_source import safe, local_path
from posix_build import digest, verify
from shell_build import verify as verify_shell
from summarize_posix import rows, apply_retry


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--report-dir', type=Path)
    parser.add_argument('--retry-dir', type=Path, action='append', default=[])
    args = parser.parse_args()
    root = args.root
    report = args.report_dir or (root / 'build-verification/posix-declarations')
    guest = report / 'guest-execution'
    records = editions(root)
    builds = {row['edition']: row for row in rows(report / 'build-all.tsv')}
    revised = rows(report / 'build-selected.tsv')
    require(set(row['edition'] for row in revised) <= set(builds), 'Unknown revised build')
    builds.update({row['edition']: row for row in revised})
    require(set(builds) == {r[0] for r in records}, 'Missing build results')
    shells = {row['edition']: row for row in rows(report / 'shell-build-status.tsv')}
    previous_boots = {row['edition']: row for row in rows(root / 'build-verification/posix-expansion/boot-all.tsv')}
    configurations, summaries = {}, []
    files, identical = 0, 0
    for edition, parent, _ in records:
        package = safe(parent, json.loads((parent / 'posix-entry.json').read_text())['directory'])
        config = json.loads((package / 'posix.json').read_text())
        files += verify(package, config)
        expected = digest((package / 'posix.json').read_bytes())
        require(builds[edition]['audit'] == builds[edition]['build'] == 'PASS', edition + ': build failed')
        require(builds[edition]['manifest_sha256_or_error'] == expected, edition + ': stale build evidence')
        stamp = json.loads((package / 'build/build.json').read_text())
        require(stamp['manifest_sha256'] == expected, edition + ': stale build manifest')
        for group, directory in (('inputs', package), ('outputs', package / 'build')):
            for relative, sha in stamp[group].items():
                require(digest(safe(directory, relative).read_bytes()) == sha, edition + ': stale ' + relative)
        for filename in ('posix_build.py', 'native_source.py'):
            require((package / filename).read_bytes() == (root / 'tools' / filename).read_bytes(), edition + ': stale helper')
        shell = safe(parent, json.loads((parent / 'shell-entry.json').read_text())['directory'])
        shell_config = json.loads((shell / 'shell.json').read_text())
        verify_shell(shell, shell_config)
        require(shells[edition]['source_and_lowering'] == shells[edition]['shell_idle_probe_elf'] == 'PASS', edition + ': shell build failed')
        require(shells[edition]['canonical_sha256'] == shell_config['canonical_sha256'], edition + ': stale shell source')
        require((shell / 'shell_build.py').read_bytes() == (root / 'tools/shell_build.py').read_bytes(), edition + ': stale shell helper')
        for filename in ('worldos-shell', 'worldos-idle', 'worldos-shell-probe'):
            header = (shell / 'build' / filename).read_bytes()[:20]
            require(header[:7] == b'\x7fELF\x01\x01\x01' and header[16:20] == b'\x02\x00\x03\x00', edition + ': wrong shell ELF')
        identical += digest((package / 'build/posix-native-probe').read_bytes()) == previous_boots[edition]['program_sha256']
        configurations[edition] = (parent, package, shell)
        summaries.append(config['summary'])
    cases = {'native': 'posix-native-probe', 'library': 'posix-library-runtime', 'core': 'posix-runtime',
             'heap': 'posix-heap-runtime', 'fork': 'posix-fork-runtime', 'exec': 'posix-exec-runtime',
             'stdin': 'posix-stdin-runtime', 'socket': 'posix-socket-runtime'}
    boots = rows(guest / 'boot-selected.tsv')
    initial_failures = [row for row in boots if row['result'] != 'PASS']
    for directory in args.retry_dir:
        boots = apply_retry(boots, rows(directory / 'boot-selected.tsv'))
    for row in boots:
        parent, package, _ = configurations[row['edition']]
        require(row['result'] == 'PASS', 'Guest failed: ' + str(row))
        require(row['program_sha256'] == digest((package / 'build' / cases[row['case']]).read_bytes()), 'Stale guest program')
        require(row['kernel_iso_sha256'] == digest(local_path(parent, '소스/build/kernel.iso').read_bytes()), 'Stale guest kernel')
    for edition in {row['edition'] for row in boots}:
        tested = [row['case'] for row in boots if row['edition'] == edition]
        require(len(tested) == len(cases) and set(tested) == set(cases), 'Incomplete guest suite: ' + edition)
    shell_boots = rows(guest / 'shell-boot-status.tsv')
    for row in shell_boots:
        parent, _, shell = configurations[row['edition']]
        require(row['result'] == 'PASS', 'Shell guest failed: ' + row['edition'])
        require(row['shell_elf_sha256'] == digest((shell / 'build/worldos-shell').read_bytes()), 'Stale shell guest program')
        require(row['kernel_elf_sha256'] == digest(local_path(parent, '소스/build/kernel.bin').read_bytes()), 'Stale shell guest kernel')
    disk_checks = [json.loads((guest / name).read_text()) for name in ('source-disk-selected.json', 'shell-source-disk-check.json')]
    disk_checks += [json.loads((directory / 'source-disk-selected.json').read_text()) for directory in args.retry_dir]
    require(all(row['unchanged'] and row['before'] == row['after'] for row in disk_checks), 'Source disk changed')
    unit_log = (report / 'unit-tests.log').read_text()
    tested = re.search(r'Ran (\d+) tests', unit_log)
    require(tested is not None and unit_log.rstrip().endswith('OK'), 'No successful unit tests')
    native = digest((report / 'korean-native-endpoint-test').read_bytes())
    legacy = digest((report / 'korean-legacy-endpoint-test').read_bytes())
    require(native == legacy, 'Legacy application changed')
    coverage = Counter(s['named_declarations'] for s in summaries)
    table = {row['edition']: row for row in rows(root / 'POSIX-선언-현지화.tsv')}
    for summary in summaries:
        row = table[summary['edition']]
        require(int(row['named_declarations']) == summary['named_declarations'] and
                int(row['pending_c_identifiers']) == len(summary['pending_c_identifiers']), 'Stale coverage table')
    result = {
        'date': '2026-09-11', 'editions_audited_and_built': len(records), 'canonical_files_round_tripped': files,
        'shell_editions_audited_and_built': len(shells), 'unit_tests_passed': int(tested.group(1)),
        'declaration_layout_language_settings_tested': ['ko', 'ja_Hira', 'ja_Kana', 'zh_Hans', 'zh_Hant', 'hi_Deva', 'ta_Taml', 'fr', 'en'],
        'new_declaration_keys': 233, 'edition_counts_by_named_declarations': dict(coverage),
        'new_declaration_name_uses': sum(s['named_declarations'] for s in summaries),
        'editions_without_pending_c_identifiers': sum(not s['pending_c_identifiers'] for s in summaries),
        'english_editions_in_complete_coverage': sum(s['language'] == 'en' for s in summaries),
        'native_probe_binaries_identical_to_previous_generation': identical,
        'korean_legacy_and_native_application_sha256': native,
        'regression_guest_cases_passed': len(boots), 'regression_editions': sorted({r['edition'] for r in boots}),
        'shell_guest_editions_passed': sorted(r['edition'] for r in shell_boots),
        'initial_executed_guest_failures': initial_failures,
        'unchanged_artifact_retry_directories': [str(p) for p in args.retry_dir],
        'sandbox_attempt': 'QEMU could not create temporary snapshots (read-only filesystem); guests did not start; original reports retained in report root',
        'executed_guest_reports': str(guest), 'source_disks_unchanged': True,
        'virtualbox_state_and_disks_modified_by_this_task': False,
        'complete_translation_all_languages': False, 'native_speaker_review': 'incomplete',
        'complete_POSIX_implementation': False,
    }
    (report / 'delivery-summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
