#!/usr/bin/env python3
"""Check current layout/build/guest evidence and write a scoped delivery report."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

from install_shells import editions
from localize_layout import plan
from native_source import local_path, safe
from posix_build import digest
from summarize_posix import rows, apply_retry


def require(value, message):
    if not value:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--backup', type=Path, required=True)
    parser.add_argument('--retry-dir', type=Path, action='append', default=[])
    args = parser.parse_args()
    root = args.root
    reports = root / 'build-verification/layout'
    guest = reports / 'guest-execution'
    records = editions(root)
    builds = {r['edition']: r for r in rows(reports / 'build-all.tsv')}
    shell_builds = {r['edition']: r for r in rows(reports / 'shell-build-status.tsv')}
    coverage = rows(root / '관리경로-현지화.tsv')
    indexed = {r['edition']: r for r in coverage}
    kernels = {r['edition']: r for r in rows(reports / 'kernel-builds.tsv')}
    require(set(builds) == set(shell_builds) == set(indexed) == {r[0] for r in records}, 'Missing edition results')
    configurations, payload_count = {}, 0
    for record in records:
        edition, parent, language = record
        migration = plan(root, record)  # Source/metadata audits, helper copies, VM entry, idempotence.
        require(migration['changes'] == 0, 'Non-idempotent layout: ' + edition)
        kernel = local_path(parent, '소스')
        require(kernel.name == indexed[edition]['source_directory'], 'Stale source-directory index')
        require(migration['status'] == indexed[edition]['review_status'], 'Wrong language-review status')
        package = safe(parent, json.loads((parent / 'posix-entry.json').read_text())['directory'])
        shell = safe(parent, json.loads((parent / 'shell-entry.json').read_text())['directory'])
        require(builds[edition]['build'] == builds[edition]['audit'] == 'PASS', 'POSIX build failed')
        manifest = digest((package / 'posix.json').read_bytes())
        require(builds[edition]['manifest_sha256_or_error'] == manifest, 'Stale build report: ' + edition)
        stamp = json.loads((package / 'build/build.json').read_text())
        require(stamp['manifest_sha256'] == manifest, 'Stale build stamp')
        for group, directory in (('inputs', package), ('outputs', package / 'build')):
            for name, expected in stamp[group].items():
                require(digest(safe(directory, name).read_bytes()) == expected, 'Stale built input/output: ' + edition + '/' + name)
        require(shell_builds[edition]['shell_idle_probe_elf'] == shell_builds[edition]['source_and_lowering'] == 'PASS', 'Shell build failed')
        for filename in ('worldos-shell', 'worldos-idle', 'worldos-shell-probe'):
            header = (shell / 'build' / filename).read_bytes()[:20]
            require(header[:7] == b'\x7fELF\x01\x01\x01' and header[16:20] == b'\x02\x00\x03\x00', 'Wrong shell ELF')
        saved = json.loads((args.backup / edition / 'migration.json').read_text())
        original = args.backup / edition / saved['old_kernel']
        require(original.is_dir(), 'Missing source backup: ' + edition)
        for path in original.rglob('*'):
            if path.is_file() and path.suffix in ('.go', '.s', '.S', '.c', '.h', '.inc', '.ld', '.sh'):
                require(path.read_bytes() == (kernel / path.relative_to(original)).read_bytes(), 'Program source changed: ' + str(path))
                payload_count += 1
        if edition in kernels:
            require(kernels[edition]['result'] == 'PASS', 'Kernel build failed')
            require(kernels[edition]['source_path'] == str(kernel.relative_to(root)), 'Stale kernel path')
            require(kernels[edition]['kernel_iso_sha256'] == digest((kernel / 'build/kernel.iso').read_bytes()), 'Stale kernel ISO')
        configurations[edition] = (kernel, package, shell)
    for row in rows(root / '문자판-목록.tsv'):
        edition = row['country'] + '/' + row['profile']
        require(row['source'] == str(configurations[edition][0].relative_to(root)), 'Stale script source index')
    programs = {'native': 'posix-native-probe', 'library': 'posix-library-runtime', 'core': 'posix-runtime',
                'heap': 'posix-heap-runtime', 'fork': 'posix-fork-runtime', 'exec': 'posix-exec-runtime',
                'stdin': 'posix-stdin-runtime', 'socket': 'posix-socket-runtime'}
    boots = rows(guest / 'boot-selected.tsv')
    initial_failures = [r for r in boots if r['result'] != 'PASS']
    for directory in args.retry_dir:
        boots = apply_retry(boots, rows(directory / 'boot-selected.tsv'))
    for row in boots:
        kernel, package, _ = configurations[row['edition']]
        require(row['edition'] in kernels and row['result'] == 'PASS', 'POSIX guest failed: ' + str(row))
        require(row['program_sha256'] == digest((package / 'build' / programs[row['case']]).read_bytes()), 'Stale guest program')
        require(row['kernel_iso_sha256'] == digest((kernel / 'build/kernel.iso').read_bytes()), 'Stale guest ISO')
    for edition in {r['edition'] for r in boots}:
        cases = [r['case'] for r in boots if r['edition'] == edition]
        require(len(cases) == len(programs) and set(cases) == set(programs), 'Incomplete POSIX guest suite')
    shell_boots = rows(guest / 'shell-boot-status.tsv')
    for row in shell_boots:
        kernel, _, shell = configurations[row['edition']]
        require(row['result'] == 'PASS' and row['edition'] in kernels, 'Shell guest failed: ' + row['edition'])
        require(row['shell_elf_sha256'] == digest((shell / 'build/worldos-shell').read_bytes()), 'Stale shell program')
        require(row['kernel_elf_sha256'] == digest((kernel / 'build/kernel.bin').read_bytes()), 'Stale shell kernel')
    disks = [json.loads((guest / name).read_text()) for name in ('source-disk-selected.json', 'shell-source-disk-check.json')]
    disks += [json.loads((directory / 'source-disk-selected.json').read_text()) for directory in args.retry_dir]
    require(all(r['unchanged'] and r['before'] == r['after'] for r in disks), 'Original disk changed')
    units = (reports / 'unit-tests.log').read_text()
    count = re.search(r'Ran (\d+) tests', units)
    require(count is not None and units.rstrip().endswith('OK'), 'No successful unit test record')
    result = {'date': '2026-09-11', 'editions': len(records),
        'review_status_counts': dict(Counter(r['review_status'] for r in coverage)),
        'english_editions_in_proposal_count': sum(r['language'] == 'en' for r in coverage),
        'management_roles': 25, 'initial_paths_renamed': sum(int(r['renamed_paths']) for r in coverage),
        'kernel_and_embedded_userspace_program_files_unchanged': payload_count,
        'layout_audit_and_idempotence_passed': len(records), 'posix_builds_passed': len(builds),
        'shell_builds_passed': len(shell_builds), 'unit_tests_passed': int(count.group(1)),
        'kernels_and_isos_rebuilt': sorted(kernels),
        'posix_guest_cases_passed': len(boots), 'posix_guest_editions': sorted({r['edition'] for r in boots}),
        'shell_guest_editions_passed': sorted(r['edition'] for r in shell_boots),
        'initial_guest_failures': initial_failures, 'same_artifact_retry_directories': [str(p) for p in args.retry_dir],
        'backup': str(args.backup), 'original_test_disks_unchanged': True,
        'existing_VirtualBox_VM_state_or_media_modified': False,
        'all_languages_fully_translated': False, 'native_speaker_review_complete': False,
        'scope': 'management paths and their consumers, not source-program renaming or document-body translation'}
    (reports / 'delivery-summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
