#!/usr/bin/env python3
"""Independent native C / host-shell template lowering and guest shell build.

No package download is needed. Only source files in this edition are read.
Standard C/POSIX ABI and literal bytes are not translated.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from native_source import tokens, safe, inverse, local_path


def c_transform(source, names, includes=None):
    includes = includes or {}
    spans = {}
    for match in re.finditer(r'(?m)^\s*#\s*include\s*([<"])([^>"\n]+)[>"]', source):
        spans[match.start(1)] = (match.end(), match.group(1) + includes.get(match.group(2), match.group(2)) + ('>' if match.group(1) == '<' else '"'))
    output, covered, number_end = [], 0, -1
    for kind, begin, end in tokens(source):
        if begin < covered:
            continue
        token = source[begin:end]
        if begin in spans:
            covered, token = spans[begin]
        elif kind == 'identifier' and not (begin == number_end and token.lower() in ('u', 'l', 'ul', 'ull', 'lu', 'llu', 'll', 'f')):
            token = names.get(token, token)
        output.append(token)
        if kind == 'number':
            number_end = end
    return ''.join(output)


def shell_transform(source, names):
    def replace(match):
        token = match.group(1)
        if token not in names:
            raise ValueError('Unregistered native shell identifier: ' + token)
        return names[token]
    # The explanatory comment's ellipsis is not a substitution.
    return re.sub(r'@\{([^{}\n]+)\}', lambda m: m.group() if m.group(1) == '...' else replace(m), source)


def load(tree):
    return json.loads((tree / 'shell.json').read_text(encoding='utf-8'))


def verify(tree, config):
    for relative, expected in config['hashes'].items():
        if hashlib.sha256(safe(tree, relative).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Shell source changed since audit: ' + str(tree / relative))
    restored = c_transform(safe(tree, config['source']).read_text(encoding='utf-8'), inverse(config['names']), inverse(config.get('includes', {})))
    if hashlib.sha256(restored.encode()).hexdigest() != config['canonical_sha256']:
        raise RuntimeError('Non-lossless C identifier lowering')
    if 'header_sha256' in config:
        restored_header = c_transform((tree / 'shell_locale.h').read_text(encoding='utf-8'), inverse(config['names']))
        if hashlib.sha256(restored_header.encode()).hexdigest() != config['header_sha256']:
            raise RuntimeError('Non-lossless command header lowering')
    restored_host = shell_transform(safe(tree, config['host_source']).read_text(encoding='utf-8'), inverse(config['host_names']))
    if hashlib.sha256(restored_host.encode()).hexdigest() != config['host_sha256']:
        raise RuntimeError('Non-lossless shell identifier lowering')
    for entry in config.get('auxiliary_sources', []):
        restored = c_transform(safe(tree, entry['source']).read_text(encoding='utf-8'), inverse(config['names']), inverse(config.get('includes', {})))
        if hashlib.sha256(restored.encode('utf-8')).hexdigest() != entry['compiler_sha256']:
            raise RuntimeError('Non-lossless auxiliary shell source: ' + entry['source'])


def source_layout(tree):
    entry = tree.parent / 'posix-entry.json'
    if entry.is_file():
        package = safe(tree.parent, json.loads(entry.read_text(encoding='utf-8'))['directory'])
        subprocess.check_call(['make', '-C', str(package), 'all'])
        return package / 'build/include', package / 'build/linker.ld', package / 'build'
    source = local_path(tree.parent, '소스')
    with local_path(source, '파일대응표.tsv').open(encoding='utf-8') as stream:
        paths = dict(list(csv.reader(stream, delimiter='\t'))[1:])
    headers = safe(source, paths['userland/posix/include/unistd.h']).parent
    linker = safe(source, paths['userland/posix/linker.ld'])
    if (source / '문자대응.json').is_file():
        subprocess.check_call(['make', '-C', str(source), 'userland'])
        library_build = source / 'build/userland'
    else:
        posix = safe(source, paths['userland/posix/Makefile']).parent
        subprocess.check_call(['make', '-C', str(posix), 'all', 'build/crt0.o'])
        library_build = posix / 'build'
    return headers, linker, library_build


def lower(tree, directory, config):
    source = safe(tree, config['source']).read_text(encoding='utf-8')
    source = c_transform(source, inverse(config['names']), inverse(config.get('includes', {})))
    (directory / 'shell.c').write_text(source, encoding='utf-8')
    header = c_transform((tree / 'shell_locale.h').read_text(encoding='utf-8'), inverse(config['names']))
    (directory / 'shell_locale.h').write_text(header, encoding='utf-8')
    host = shell_transform(safe(tree, config['host_source']).read_text(encoding='utf-8'), inverse(config['host_names']))
    (directory / 'build-shell.sh').write_text(host, encoding='utf-8')
    subprocess.check_call(['sh', '-n', str(directory / 'build-shell.sh')])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['build', 'verify', 'host-build'])
    parser.add_argument('--tree', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    tree = args.tree.resolve()
    config = load(tree)
    if args.action == 'verify':
        verify(tree, config)
        print('PASS', config['edition'], 'shell source and lowering')
        return
    build = safe(tree, 'build')
    build.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='shell-stage-', dir=str(build)) as temporary:
        stage = Path(temporary)
        lower(tree, stage, config)
        artifact = stage / 'worldos-shell'
        if args.action == 'host-build':
            subprocess.check_call(['gcc', '-std=c99', '-D_POSIX_C_SOURCE=200809L', '-Wall', '-Wextra', '-Werror',
                                   str(stage / 'shell.c'), '-o', str(artifact)])
            output = safe(build, 'host-shell')
        else:
            headers, linker, library_build = source_layout(tree)
            subprocess.check_call(['sh', str(stage / 'build-shell.sh'), str(stage / 'shell.c'),
                str(stage / 'shell.o'), str(artifact), str(headers), str(library_build / 'crt0.o'),
                str(library_build / 'libposix.a'), str(linker)])
            output = safe(build, 'worldos-shell')
            for filename, executable in [('idle.c', 'worldos-idle'), ('probe.c', 'worldos-shell-probe')]:
                auxiliary = next((entry for entry in config.get('auxiliary_sources', []) if entry['compiler'] == filename), None)
                if auxiliary:
                    text = safe(tree, auxiliary['source']).read_text(encoding='utf-8')
                    (stage / filename).write_text(c_transform(text, inverse(config['names']), inverse(config.get('includes', {}))), encoding='utf-8')
                else:
                    shutil.copy2(str(safe(tree, filename)), str(stage / filename))
                subprocess.check_call(['sh', str(stage / 'build-shell.sh'), str(stage / filename),
                    str(stage / (filename + '.o')), str(stage / executable), str(headers),
                    str(library_build / 'crt0.o'), str(library_build / 'libposix.a'), str(linker)])
                os.replace(str(stage / executable), str(safe(build, executable)))
        os.replace(str(artifact), str(output))
    print('PASS', config['edition'], args.action)


if __name__ == '__main__':
    main()
