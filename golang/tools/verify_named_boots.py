#!/usr/bin/env python3
"""Boot selected named kernels against disposable copies of a supplied test disk.

The original disk is read only. Guest writes use QEMU snapshots. Monitor commands
use a private stdin pipe, not a host socket. Logs remain in build-verification.
"""
import argparse
import csv
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
from native_source import local_path


def run(command, **kwargs):
    return subprocess.check_output([str(x) for x in command], stderr=subprocess.STDOUT, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--disk', required=True, type=Path)
    parser.add_argument('--idle', required=True, type=Path)
    parser.add_argument('--country', action='append', default=[])
    parser.add_argument('--variant', action='append', default=[], help='independent script edition, e.g. IND/hi_Deva')
    parser.add_argument('--all-script-variants', action='store_true')
    parser.add_argument('--use-built-iso', action='store_true', help='use already verified ISO instead of rebuilding')
    parser.add_argument('--full-suite', action='store_true')
    parser.add_argument('--append-results', action='store_true', help='keep earlier country results in this test batch')
    args = parser.parse_args()
    if args.all_script_variants:
        if args.variant:
            parser.error('choose --variant or --all-script-variants, not both')
        from generate_script_variants import profiles
        args.variant = [record[0] + '/' + record[1] for record in profiles()]
    if args.country and args.variant:
        parser.error('choose --country or --variant, not both')
    if not args.disk.is_file() or not args.idle.is_file():
        parser.error('disk and idle executable must be existing regular files')
    log_root = args.root / 'build-verification'
    log_root.mkdir(exist_ok=True)
    cases = [('core', 'posix-runtime', b'POSIX-CORE:PASS')]
    if args.full_suite:
        cases += [('heap', 'posix-heap-runtime', b'POSIX-HEAP:PASS'),
                  ('fork', 'posix-fork-runtime', b'POSIX-FORK:PASS'),
                  ('exec', 'posix-exec-runtime', b'PTEST:PASS:cloexec'),
                  ('stdin', 'posix-stdin-runtime', b'POSIX-STDIN:PASS'),
                  ('socket', 'posix-socket-runtime', b'NTEST:PASS:close-server')]
    results = []
    status_name = 'script-boot-status.tsv' if args.variant else 'named-boot-status.tsv'
    if args.append_results and (log_root / status_name).is_file():
        with (log_root / status_name).open(encoding='utf-8') as previous:
            results = list(csv.reader(previous, delimiter='\t'))[1:]
    with tempfile.TemporaryDirectory(prefix='worldos-named-boot-') as temporary:
        raw = Path(temporary) / 'disk.raw'
        run(['qemu-img', 'convert', '-O', 'raw', args.disk, raw])
        layout = run(['sfdisk', '-d', raw]).decode()
        match = re.search(r'start=\s*(\d+)', layout)
        if not match or int(match.group(1)) <= 0:
            raise RuntimeError('No partition offset in supplied test disk')
        image = str(raw) + '@@' + str(int(match.group(1)) * 512)
        environment = dict(os.environ, MTOOLS_SKIP_CHECK='1')
        for slot in ('USER2', 'USER3'):
            run(['mcopy', '-o', '-i', image, args.idle, '::' + slot], env=environment)
        for selection in args.variant or args.country or ['KOR', 'USA', 'JPN', 'CHN', 'ARE', 'DEU', 'IND']:
            if args.variant:
                if not re.fullmatch(r'[A-Z]{3}/[a-z]{2,3}_[A-Z][a-z]{3}', selection):
                    raise RuntimeError('Invalid script edition: ' + selection)
                country = selection.replace('/', '-')
                tree = local_path(args.root / '문자판' / selection, '소스')
                user_build = tree / 'build/userland'
            else:
                country = selection
                if not re.fullmatch(r'[A-Z]{3}', country):
                    raise RuntimeError('Invalid country code')
                tree = local_path(args.root / '나라' / country, '소스')
                with local_path(tree, '파일대응표.tsv').open(encoding='utf-8') as source_map:
                    mapping = dict(list(csv.reader(source_map, delimiter='\t'))[1:])
                user_build = (tree / mapping['userland/posix/Makefile']).parent / 'build'
            if not args.use_built_iso:
                iso_output = run(['make', '-C', tree, 'iso'])
                (log_root / ('boot-' + country + '-iso.log')).write_bytes(iso_output)
            for case, program, expected in cases:
                run(['mcopy', '-o', '-i', image, user_build / program, '::USER1'], env=environment)
                if case == 'exec':
                    run(['mcopy', '-o', '-i', image, user_build / 'posix-exec-target', '::PXEXEC'], env=environment)
                serial = log_root / ('boot-' + country + '-' + case + '.serial')
                diagnostics = log_root / ('boot-' + country + '-' + case + '.qemu')
                # Empty only this test's exact output file, never a guest/user disk.
                serial.write_bytes(b'')
                with diagnostics.open('wb') as log:
                    process = subprocess.Popen(['qemu-system-x86_64', '-boot', 'd', '-m', '512',
                        '-display', 'none', '-serial', 'file:' + str(serial), '-monitor', 'stdio', '-no-reboot',
                        '-drive', 'file=' + str(tree / 'build/kernel.iso') + ',media=cdrom,if=none,id=cd0',
                        '-device', 'ide-cd,drive=cd0,bus=ide.1,unit=0',
                        '-drive', 'file=' + str(raw) + ',format=raw,if=none,id=disk0,snapshot=on',
                        '-device', 'ide-hd,drive=disk0,bus=ide.0,unit=1'],
                        stdin=subprocess.PIPE, stdout=log, stderr=subprocess.STDOUT)
                    passed, sent = False, False
                    try:
                        deadline = time.monotonic() + 90
                        while time.monotonic() < deadline:
                            contents = serial.read_bytes()
                            if re.search(b'PTEST:FAIL|NTEST:FAIL|POSIX-[A-Z]+:FAIL|EXCEPTION vec=|HALTED AFTER EXCEPTION|panic|fatal', contents):
                                break
                            if expected in contents:
                                passed = True
                                break
                            if case == 'stdin' and b'POSIX-STDIN:READY' in contents and not sent:
                                process.stdin.write(b'sendkey a\nsendkey ret\n')
                                process.stdin.flush()
                                sent = True
                            if process.poll() is not None:
                                break
                            time.sleep(0.2)
                    finally:
                        if process.poll() is None:
                            process.stdin.write(b'quit\n')
                            process.stdin.flush()
                            try:
                                process.wait(timeout=5)
                            except subprocess.TimeoutExpired:
                                process.terminate()
                                process.wait(timeout=5)
                        process.stdin.close()
                results = [row for row in results if row[:2] != [country, case]]
                results.append([country, case, 'PASS' if passed else 'FAIL', expected.decode()])
                print('{} {}: {}'.format(country, case, 'PASS' if passed else 'FAIL'), flush=True)
                with (log_root / status_name).open('w', encoding='utf-8', newline='') as status:
                    writer = csv.writer(status, delimiter='\t', lineterminator='\n')
                    writer.writerow(['country', 'test', 'result', 'expected_marker'])
                    writer.writerows(results)
                if not passed:
                    raise RuntimeError('Boot test failed; see ' + str(serial) + ' and ' + str(diagnostics))


if __name__ == '__main__':
    main()
