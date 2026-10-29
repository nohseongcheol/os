#!/usr/bin/env python3
"""Boot guest shells using private disks; check native commands, exec and UDP."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

from install_shells import editions
from generate_script_variants import table
from shell_disk import find_shell, install_programs, run
from native_source import local_path


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def test_script(config, commands_only=False):
    aliases = config['commands']
    def command(name, arguments=''):
        return aliases[name] + (' ' + arguments if arguments else '') + '\n'
    return ('# Explicit native command aliases and UTF-8 payload\n'
        + command('echo', '"WORLDOS-SHELL:NATIVE 한글 हिन्दी தமிழ்"')
        + command('echo', 'prefix" joined" a\\ b "" tail')
        + command('pwd') + command('cd', '/') + command('stat', '/SHTEXT')
        + command('cat', '/SHTEXT') + command('pid') + command('uname')
        + ('' if commands_only else command('run', '/SHEXEC "argument with spaces"'))
        + command('udp', '"WORLDOS-SHELL:UDP"')
        + command('source', '/SHNEST')
        + 'echo NEVER_EXECUTE "unterminated\n'
        + 'echo NEVER_EXECUTE ' + 'x ' * 20 + '\n'
        + 'echo NEVER_EXECUTE ' + 'x' * 600 + '\n'
        + command('echo', 'WORLDOS-SHELL:COMPLETE')
        + command('exit'))


def boot(root, edition, base, rebuild=False, commands_only=False, timeout=75, dump_memory=False, report_root=None):
    parent, package = find_shell(root, edition)
    config = json.loads((package / 'shell.json').read_text(encoding='utf-8'))
    iso = local_path(parent, '소스/build/kernel.iso')
    logs = (report_root or (root / 'build-verification')) / 'shell-boots'
    logs.mkdir(parents=True, exist_ok=True)
    label = edition.replace('/', '-') + ('-commands-only' if commands_only else '')
    if rebuild or not iso.is_file():
        output = run(['make', '-B', '-C', local_path(parent, '소스'), 'iso'])
        (logs / (label + '-kernel.log')).write_bytes(output)
    serial, diagnostics = logs / (label + '.serial'), logs / (label + '.qemu')
    passed = False
    with tempfile.TemporaryDirectory(prefix='worldos-shell-boot-') as temporary:
        stage = Path(temporary)
        raw = stage / 'disk.raw'
        shutil.copyfile(str(base), str(raw))
        (stage / 'script').write_text(test_script(config, commands_only), encoding='utf-8')
        (stage / 'nested').write_text(config['commands']['echo'] + ' WORLDOS-SHELL:NESTED\n', encoding='utf-8')
        (stage / 'text').write_text('WORLDOS-SHELL:FILE-CONTENT\n', encoding='utf-8')
        install_programs(raw, package, [(stage / 'script', 'SHTEST'), (stage / 'nested', 'SHNEST'), (stage / 'text', 'SHTEXT')])
        serial.write_bytes(b'')
        with diagnostics.open('wb') as log:
            process = subprocess.Popen(['qemu-system-x86_64', '-boot', 'd', '-m', '512', '-display', 'none',
                '-serial', 'file:' + str(serial), '-monitor', 'stdio', '-no-reboot',
                '-drive', 'file=' + str(iso) + ',media=cdrom,if=none,id=cd0',
                '-device', 'ide-cd,drive=cd0,bus=ide.1,unit=0',
                '-drive', 'file=' + str(raw) + ',format=raw,if=none,id=disk0,snapshot=on',
                '-device', 'ide-hd,drive=disk0,bus=ide.0,unit=1'],
                stdin=subprocess.PIPE, stdout=log, stderr=subprocess.STDOUT)
            sent = False
            try:
                deadline = time.monotonic() + timeout
                while time.monotonic() < deadline:
                    content = serial.read_bytes()
                    if b'WORLDOS-SHELL:EXIT' in content:
                        markers = ['WORLDOS-SHELL:NATIVE 한글 हिन्दी தமிழ்', 'prefix joined a b  tail',
                            'WORLDOS-SHELL:FILE-CONTENT',
                            'udp-received: WORLDOS-SHELL:UDP', 'WORLDOS-SHELL:NESTED',
                            'syntax error:', 'input rejected:', 'WORLDOS-SHELL:COMPLETE']
                        if not commands_only:
                            markers += ['WORLDOS-SHELL-PROBE:PASS', 'exit-status=7']
                        passed = all(marker.encode() in content for marker in markers) and b'NEVER_EXECUTE' not in content
                        break
                    if re.search(b'EXCEPTION vec=|HALTED AFTER EXCEPTION|panic|fatal|WORLDOS-SHELL-PROBE:FAIL', content):
                        break
                    if not sent and b'WORLDOS-SHELL:READY' in content:
                        # File contents carry native input; hardware key mapping is ASCII.
                        keys = ['s', 'o', 'u', 'r', 'c', 'e', 'spc', 'slash', 's', 'h', 't', 'e', 's', 't', 'ret']
                        for key in keys:
                            process.stdin.write(('sendkey ' + key + ' 50\n').encode())
                            process.stdin.flush()
                            time.sleep(0.15)
                        sent = True
                    if process.poll() is not None:
                        break
                    time.sleep(0.05)
            finally:
                if process.poll() is None:
                    try:
                        if not passed:
                            process.stdin.write(b'stop\ninfo registers\ninfo tlb\n')
                            if dump_memory:
                                for address, size, suffix in [(0x00900000, 0x00200000, 'globals'), (0x01200000, 0x00800000, 'heap')]:
                                    destination = logs / (label + '-' + suffix + '.memory')
                                    process.stdin.write(('pmemsave 0x%x 0x%x "%s"\n' % (address, size, destination)).encode())
                            process.stdin.flush()
                            time.sleep(0.2)
                        process.stdin.write(b'quit\n')
                        process.stdin.flush()
                        process.wait(timeout=5)
                    except (BrokenPipeError, subprocess.TimeoutExpired):
                        process.terminate()
                        process.wait(timeout=5)
                process.stdin.close()
    print(edition, 'shell boot', 'PASS' if passed else 'FAIL', flush=True)
    return [edition, 'PASS' if passed else 'FAIL', config['canonical_sha256'], digest(package / 'build/worldos-shell'), digest(local_path(parent, '소스/build/kernel.bin'))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--disk', required=True, type=Path)
    parser.add_argument('--edition', action='append', default=[])
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--rebuild-kernels', action='store_true')
    parser.add_argument('--commands-only', action='store_true', help='diagnostic: omit fork+exec; keep a separate result report')
    parser.add_argument('--timeout', type=int, default=75, help='seconds allowed after starting QEMU')
    parser.add_argument('--dump-memory', action='store_true', help='save guest globals/heap on failure for diagnosis')
    parser.add_argument('--jobs', type=int, default=2, choices=range(1, 5), help='parallel guest/build workers (default: 2)')
    parser.add_argument('--report-dir', type=Path, help='keep this verification generation separate from earlier results')
    args = parser.parse_args()
    if args.timeout < 5:
        parser.error('timeout must be at least five seconds')
    if not args.disk.is_file():
        parser.error('an existing source disk is required')
    available = {record[0] for record in editions(args.root)}
    selected = sorted(available) if args.all else args.edition or ['KOR', 'USA', 'JPN', 'CHN', 'ARE', 'DEU', 'IND', 'IND/ta_Taml', 'JPN/ja_Hira', 'JPN/ja_Kana', 'CHN/zh_Hant']
    if set(selected) - available:
        parser.error('unknown edition')
    before = digest(args.disk)
    report_root = args.report_dir or (args.root / 'build-verification')
    report_root.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix='worldos-shell-base-') as temporary:
        base = Path(temporary) / 'base.raw'
        run(['qemu-img', 'convert', '-O', 'raw', args.disk, base])
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(lambda edition: boot(args.root, edition, base, args.rebuild_kernels, args.commands_only, args.timeout, args.dump_memory, report_root), selected))
    if digest(args.disk) != before:
        raise RuntimeError('Source disk changed during verification')
    report = report_root / ('shell-commands-only-status.tsv' if args.commands_only else 'shell-boot-status.tsv')
    previous = {}
    if report.exists():
        with report.open(encoding='utf-8') as stream:
            previous = {row[0]: row for row in list(csv.reader(stream, delimiter='\t'))[1:]}
    previous.update({row[0]: row for row in results})
    report.write_text(table(['edition', 'result', 'canonical_sha256', 'shell_elf_sha256', 'kernel_elf_sha256'], sorted(previous.values())), encoding='utf-8')
    (report.parent / 'shell-source-disk-check.json').write_text(json.dumps({'path': str(args.disk), 'before': before, 'after': digest(args.disk), 'unchanged': True}, indent=2) + '\n')
    if any(row[1] != 'PASS' for row in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
