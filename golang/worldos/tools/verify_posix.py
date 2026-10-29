#!/usr/bin/env python3
"""Audit, compile, and optionally boot independent native POSIX packages."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

from generate_script_variants import table
from install_shells import editions
from native_source import safe, local_path
from posix_build import digest, verify


def command(arguments, **kwargs):
    return subprocess.check_output([str(item) for item in arguments], stderr=subprocess.STDOUT, **kwargs)


def boot(args, record, package, report_root):
    edition, parent, _ = record
    kernel = local_path(parent, '소스/build/kernel.iso')
    if not kernel.is_file():
        raise RuntimeError('Build this edition kernel ISO before boot verification')
    cases = [('native', 'posix-native-probe', b'POSIX-NATIVE:PASS')]
    if args.full_suite:
        cases += [('library', 'posix-library-runtime', b'POSIX-LIBRARY:PASS'),
                  ('core', 'posix-runtime', b'POSIX-CORE:PASS'),
                  ('heap', 'posix-heap-runtime', b'POSIX-HEAP:PASS'),
                  ('fork', 'posix-fork-runtime', b'POSIX-FORK:PASS'),
                  ('exec', 'posix-exec-runtime', b'PTEST:PASS:cloexec'),
                  ('stdin', 'posix-stdin-runtime', b'POSIX-STDIN:PASS'),
                  ('socket', 'posix-socket-runtime', b'NTEST:PASS:close-server')]
    results = []
    with tempfile.TemporaryDirectory(prefix='worldos-posix-boot-') as temporary:
        raw = Path(temporary) / 'disk.raw'
        command(['qemu-img', 'convert', '-O', 'raw', args.disk, raw])
        layout = command(['sfdisk', '-d', raw]).decode()
        match = re.search(r'start=\s*(\d+)', layout)
        if not match or int(match.group(1)) <= 0:
            raise RuntimeError('No FAT partition start in test disk')
        partition = str(raw) + '@@' + str(int(match.group(1)) * 512)
        environment = dict(os.environ, MTOOLS_SKIP_CHECK='1')
        for slot in ('USER2', 'USER3'):
            command(['mcopy', '-o', '-i', partition, args.idle, '::' + slot], env=environment)
        for case, program, marker in cases:
            executable = package / 'build' / program
            command(['mcopy', '-o', '-i', partition, executable, '::USER1'], env=environment)
            if case == 'exec':
                command(['mcopy', '-o', '-i', partition, package / 'build/posix-exec-target', '::PXEXEC'], env=environment)
            filename = edition.replace('/', '-') + '-' + case
            serial = report_root / (filename + '.serial')
            serial.write_bytes(b'')
            with (report_root / (filename + '.qemu')).open('wb') as diagnostics:
                process = subprocess.Popen(['qemu-system-x86_64', '-boot', 'd', '-m', '512',
                    '-display', 'none', '-serial', 'file:' + str(serial), '-monitor', 'stdio', '-no-reboot',
                    '-drive', 'file=' + str(kernel) + ',media=cdrom,if=none,id=cd0',
                    '-device', 'ide-cd,drive=cd0,bus=ide.1,unit=0',
                    '-drive', 'file=' + str(raw) + ',format=raw,if=none,id=disk0,snapshot=on',
                    '-device', 'ide-hd,drive=disk0,bus=ide.0,unit=1'],
                    stdin=subprocess.PIPE, stdout=diagnostics, stderr=subprocess.STDOUT)
                passed, sent, first_pass = False, False, None
                try:
                    deadline = time.monotonic() + args.timeout
                    while time.monotonic() < deadline:
                        contents = serial.read_bytes()
                        if re.search(b'PTEST:FAIL|NTEST:FAIL|POSIX-[A-Z]+:FAIL|EXCEPTION vec=|HALTED AFTER EXCEPTION|panic|fatal', contents):
                            break
                        if marker in contents:
                            if first_pass is None:
                                first_pass = time.monotonic()
                            if time.monotonic() - first_pass >= 0.5:
                                passed = True
                                break
                        if case == 'stdin' and b'POSIX-STDIN:READY' in contents and not sent:
                            process.stdin.write(b'sendkey a\nsendkey ret\n')
                            process.stdin.flush()
                            sent = True
                        if process.poll() is not None:
                            break
                        time.sleep(0.1)
                finally:
                    if process.poll() is None:
                        try:
                            process.stdin.write(b'quit\n')
                            process.stdin.flush()
                            process.wait(timeout=5)
                        except (BrokenPipeError, subprocess.TimeoutExpired):
                            process.kill()
                            process.wait()
                    process.stdin.close()
                results.append([edition, case, 'PASS' if passed else 'FAIL', digest(executable.read_bytes()), digest(kernel.read_bytes())])
    return results


def check(args, record, logs):
    edition, parent, _ = record
    entry = json.loads((parent / 'posix-entry.json').read_text(encoding='utf-8'))
    package = safe(parent, entry['directory'])
    config = json.loads((package / 'posix.json').read_text(encoding='utf-8'))
    verify(package, config)
    if args.build:
        try:
            output = command(['make', '-C', package, 'all'])
        except subprocess.CalledProcessError as error:
            (logs / (edition.replace('/', '-') + '.build.log')).write_bytes(error.output)
            raise
        (logs / (edition.replace('/', '-') + '.build.log')).write_bytes(output)
    if args.build or args.boot:
        stamp = json.loads((package / 'build/build.json').read_text(encoding='utf-8'))
        if stamp['manifest_sha256'] != digest((package / 'posix.json').read_bytes()):
            raise RuntimeError('Stale POSIX build manifest: ' + edition)
        for relative, expected in stamp['inputs'].items():
            if digest(safe(package, relative).read_bytes()) != expected:
                raise RuntimeError('Stale POSIX input: ' + relative)
        for relative, expected in stamp['outputs'].items():
            if digest(safe(package / 'build', relative).read_bytes()) != expected:
                raise RuntimeError('Modified POSIX artifact: ' + relative)
        for filename in ('posix-runtime', 'posix-native-probe'):
            header = (package / 'build' / filename).read_bytes()[:20]
            if header[:6] != b'\x7fELF\x01\x01' or header[16:20] != b'\x02\x00\x03\x00':
                raise RuntimeError('Not an ELF32 i386 executable')
    boot_rows = boot(args, record, package, logs) if args.boot else []
    return [edition, 'PASS', 'PASS' if args.build else 'NOT_RUN', digest((package / 'posix.json').read_bytes())], boot_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', action='append', default=[])
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--boot', action='store_true')
    parser.add_argument('--full-suite', action='store_true')
    parser.add_argument('--disk', type=Path)
    parser.add_argument('--idle', type=Path)
    parser.add_argument('--jobs', type=int, default=2, choices=range(1, 5))
    parser.add_argument('--timeout', type=int, default=90)
    parser.add_argument('--report-dir', type=Path, help='separate report directory for a new verification generation')
    args = parser.parse_args()
    records = editions(args.root)
    if set(args.edition) - {r[0] for r in records}:
        parser.error('Unknown edition')
    if args.boot and (not args.disk or not args.disk.is_file() or not args.idle or not args.idle.is_file()):
        parser.error('--boot requires existing --disk and --idle files')
    if args.full_suite and not args.boot:
        parser.error('--full-suite requires --boot')
    before = digest(args.disk.read_bytes()) if args.boot else None
    logs = args.report_dir or (args.root / 'build-verification/posix')
    logs.mkdir(parents=True, exist_ok=True)
    results, boots, failed = [], [], False
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(check, args, record, logs): record[0] for record in records if not args.edition or record[0] in args.edition}
        for future in as_completed(futures):
            edition = futures[future]
            try:
                result, boot_rows = future.result()
                results.append(result)
                boots.extend(boot_rows)
                failed = failed or any(row[2] != 'PASS' for row in boot_rows)
                print('PASS' if all(row[2] == 'PASS' for row in boot_rows) else 'FAIL', edition, 'audit/build' if args.build else 'audit', len(boot_rows), 'guest cases', flush=True)
            except Exception as error:
                failed = True
                results.append([edition, 'FAIL', 'FAIL' if args.build else 'NOT_RUN', str(error)])
                print('FAIL', edition, str(error), flush=True)
    mode = 'build' if args.build else 'audit'
    suffix = '-selected' if args.edition else '-all'
    (logs / (mode + suffix + '.tsv')).write_text(table(['edition', 'audit', 'build', 'manifest_sha256_or_error'], sorted(results)), encoding='utf-8')
    if args.boot:
        (logs / ('boot' + suffix + '.tsv')).write_text(table(['edition', 'case', 'result', 'program_sha256', 'kernel_iso_sha256'], sorted(boots)), encoding='utf-8')
        after = digest(args.disk.read_bytes())
        (logs / ('source-disk' + suffix + '.json')).write_text(json.dumps({'source': str(args.disk), 'before': before, 'after': after, 'unchanged': before == after}, indent=2) + '\n')
        failed = failed or before != after
    raise SystemExit(1 if failed else 0)


if __name__ == '__main__':
    main()
