#!/usr/bin/env python3
"""Build this edition's native POSIX sources; never read a donor source tree."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from native_source import tokens, safe, inverse, local_path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def c_transform(source, names, includes=None):
    """Rewrite identifiers and exact include operands, never literals/comments.

    Header names are preprocessing tokens, not C identifiers (read.h, sys/stat.h).
    Numeric suffixes such as 1UL must not be rewritten as identifiers either.
    """
    includes = includes or {}
    spans = {}
    for match in re.finditer(r'(?m)^\s*#\s*include\s*([<"])([^>"\n]+)[>"]', source):
        spans[match.start(1)] = (match.end(), match.group(1) + includes.get(match.group(2), match.group(2)) + ('>' if match.group(1) == '<' else '"'))
    output, covered, number_end = [], 0, -1
    for kind, begin, end in tokens(source):
        if begin < covered:
            continue
        if begin in spans:
            covered, text = spans[begin]
            output.append(text)
        else:
            text = source[begin:end]
            if kind == 'identifier' and not (begin == number_end and text.lower() in ('u', 'l', 'ul', 'ull', 'lu', 'llu', 'll', 'f')):
                text = names.get(text, text)
            output.append(text)
        if kind == 'number':
            number_end = end
    return ''.join(output)


def c_identifiers(source):
    """Actual C identifiers, excluding include paths and integer suffixes."""
    includes = [(m.start(1), m.end()) for m in re.finditer(
        r'(?m)^\s*#\s*include\s*([<"])([^>"\n]+)[>"]', source)]
    result, number_end = set(), -1
    for kind, begin, end in tokens(source):
        if any(start <= begin < stop for start, stop in includes):
            continue
        text = source[begin:end]
        if kind == 'identifier' and not (begin == number_end and text.lower() in ('u', 'l', 'ul', 'ull', 'lu', 'llu', 'll', 'f')):
            result.add(text)
        number_end = end if kind == 'number' else -1
    return result


def application_maps(config):
    names, includes = inverse(config['names']), inverse(config['includes'])
    for target, aliases in ((names, config.get('name_aliases', {})), (includes, config.get('include_aliases', {}))):
        for native, standard in aliases.items():
            if native in target and target[native] != standard:
                raise ValueError('Ambiguous legacy native name: ' + native)
            target[native] = standard
    return names, includes


def lower(data, entry, config):
    if entry['kind'] != 'c':
        return data
    return c_transform(data.decode('utf-8'), inverse(config['names']), inverse(config['includes'])).encode('utf-8')


def verify(tree, config):
    for relative, expected in config['hashes'].items():
        if digest(safe(tree, relative).read_bytes()) != expected:
            raise RuntimeError('Modified audited POSIX file: ' + str(tree / relative))
    for entry in config['files']:
        data = safe(tree, entry['native']).read_bytes()
        if digest(lower(data, entry, config)) != entry['compiler_sha256']:
            raise RuntimeError('POSIX source does not round-trip: ' + entry['native'])
    return len(config['files'])


def build(tree, config):
    output = safe(tree, 'build')
    output.mkdir(exist_ok=True)
    with safe(output, '.posix-build.lock').open('a') as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        _build(tree, config)


def _build(tree, config):
    output = safe(tree, 'build')
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='posix-stage-', dir=str(output)) as temporary:
        stage = Path(temporary)
        for entry in config['files']:
            target = safe(stage, entry['compiler'])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(lower(safe(tree, entry['native']).read_bytes(), entry, config))
        subprocess.check_call(['make', '-B', '-C', str(stage), 'test-programs', 'check'])
        flags = ['gcc', '-m32', '-ffreestanding', '-fno-pie', '-fno-pic', '-fno-stack-protector', '-fno-builtin', '-Wall', '-Wextra', '-Werror', '-nostdinc', '-I' + str(stage / 'include')]
        for name in ('library', 'library_main'):
            subprocess.check_call(flags + ['-c', str(stage / ('tests/' + name + '.c')), '-o', str(stage / ('build/' + name + '.o'))])
        subprocess.check_call(['ld', '-n', '-m', 'elf_i386', '-e', '_start', '-T', str(stage / 'linker.ld'), '-static', '--no-ld-generated-unwind-info', '-o', str(stage / 'build/posix-library-runtime'), str(stage / 'build/crt0.o'), str(stage / 'build/library_main.o'), str(stage / 'build/library.o'), str(stage / 'build/libposix.a')])
        subprocess.check_call(flags + ['-c', str(stage / 'tests/probe.c'), '-o', str(stage / 'build/probe.o')])
        subprocess.check_call(['ld', '-n', '-m', 'elf_i386', '-e', '_start', '-T', str(stage / 'linker.ld'), '-static', '--no-ld-generated-unwind-info', '-o', str(stage / 'build/posix-native-probe'), str(stage / 'build/crt0.o'), str(stage / 'build/probe.o'), str(stage / 'build/library.o'), str(stage / 'build/libposix.a')])
        symbols = subprocess.check_output(['nm', '-g', '--defined-only', str(stage / 'build/libposix.a')]).decode()
        if '__syscall6' not in symbols or '__syscall_result' not in symbols or 'engos' in symbols.lower():
            raise RuntimeError('Wrong POSIX implementation namespace')
        # Every public entry in the manifest must have a real defined symbol.
        names_file = local_path(tree, '이름대응.tsv').read_text(encoding='utf-8').splitlines()[1:]
        public = {line.split('\t')[0] for line in names_file if line.split('\t')[2] == 'function'}
        defined = {line.split()[-1] for line in symbols.splitlines() if len(line.split()) == 3}
        if public - defined:
            raise RuntimeError('Missing public implementations: ' + repr(sorted(public - defined)))
        subprocess.check_call(['ld', '-m', 'elf_i386', '-r', '--whole-archive', str(stage / 'build/libposix.a'), '--no-whole-archive', '-o', str(stage / 'build/all-posix.o')])
        if subprocess.check_output(['nm', '-u', str(stage / 'build/all-posix.o')]).strip():
            raise RuntimeError('Unresolved POSIX implementation symbol')
        for path in (stage / 'build').iterdir():
            if path.is_file():
                destination = safe(output, path.name)
                with tempfile.NamedTemporaryFile(dir=str(output), delete=False) as stream:
                    staging = Path(stream.name)
                shutil.copy2(str(path), str(staging))
                os.replace(str(staging), str(destination))
        # Compiler-facing standard headers are output, not authoritative sources.
        for path in (stage / 'include').rglob('*.h'):
            target = safe(output, 'include/' + str(path.relative_to(stage / 'include')))
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(path), str(target))
        shutil.copy2(str(stage / 'linker.ld'), str(output / 'linker.ld'))
    stamp = {'manifest_sha256': digest((tree / 'posix.json').read_bytes()),
             'inputs': {entry['native']: digest(safe(tree, entry['native']).read_bytes()) for entry in config['files']},
             'outputs': {path.name: digest(path.read_bytes()) for path in output.iterdir() if path.is_file() and path.name not in ('build.json', '.posix-build.lock')}}
    (output / 'build.json').write_text(json.dumps(stamp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['build', 'verify', 'compile'])
    parser.add_argument('--tree', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--source', type=Path, help='native C application source')
    parser.add_argument('--output', type=Path, help='new ELF output path')
    args = parser.parse_args()
    tree = args.tree.resolve()
    config = json.loads((tree / 'posix.json').read_text(encoding='utf-8'))
    if args.action == 'verify':
        print('PASS', config['edition'], verify(tree, config), 'native POSIX source files')
        return
    if args.action == 'compile' and (not args.source or not args.output or args.output.exists() or args.output.is_symlink()):
        parser.error('compile requires --source and a NEW --output')
    build(tree, config)
    if args.action == 'compile':
        with tempfile.TemporaryDirectory(prefix='posix-application-') as temporary:
            temporary = Path(temporary)
            source = temporary / 'application.c'
            names, includes = application_maps(config)
            source.write_text(c_transform(args.source.read_text(encoding='utf-8'), names, includes), encoding='utf-8')
            subprocess.check_call(['gcc', '-m32', '-nostdinc', '-ffreestanding', '-fno-pie', '-fno-stack-protector', '-fno-builtin', '-Wall', '-Wextra', '-Werror', '-I' + str(tree / 'build/include'), '-c', str(source), '-o', str(temporary / 'application.o')])
            executable = temporary / 'application'
            subprocess.check_call(['ld', '-n', '-m', 'elf_i386', '-e', '_start', '-T', str(tree / 'build/linker.ld'), '-static', '--no-ld-generated-unwind-info', '-o', str(executable), str(tree / 'build/crt0.o'), str(temporary / 'application.o'), str(tree / 'build/libposix.a')])
            # Exclusive creation: never replace the user's executable.
            with args.output.open('xb') as stream:
                stream.write(executable.read_bytes())
    print('PASS', config['edition'], 'native POSIX build')


if __name__ == '__main__':
    main()
