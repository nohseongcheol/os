#!/usr/bin/env python3
"""WorldOS native-identifier dialect adapter (Python 3.6+, no extra packages).

Source names may contain combining marks; standard Go 1.10 cannot parse them.
Only lexical identifiers/import paths are lowered. Strings, comments and C ABI
are not translated. The source tree, not a cached donor tree, is authoritative.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata


def start(ch):
    return ch == '_' or unicodedata.category(ch).startswith('L')


def continuation(ch):
    return start(ch) or unicodedata.category(ch).startswith('M') or unicodedata.category(ch) == 'Nd' or ch in '\u200c\u200d'


def tokens(source):
    """Yield exact spans; numeric literals must never be identifier-rewritten."""
    i = 0
    while i < len(source):
        begin = i
        if source.startswith('//', i):
            end = source.find('\n', i)
            i = len(source) if end < 0 else end
            kind = 'comment'
        elif source.startswith('/*', i):
            end = source.find('*/', i + 2)
            if end < 0:
                raise ValueError('Unclosed block comment')
            i, kind = end + 2, 'comment'
        elif source[i] in '\"\'`':
            quote = source[i]
            i += 1
            while i < len(source):
                if source[i] == quote:
                    i += 1
                    break
                if source[i] == '\\' and quote != '`':
                    i += 1
                i += 1
            else:
                raise ValueError('Unclosed literal')
            kind = 'string' if quote != "'" else 'rune'
        elif source[i].isdigit() and ord(source[i]) < 128 or (source[i] == '.' and i + 1 < len(source) and source[i + 1].isdigit()):
            # Includes exponent signs, hex digits and imaginary suffixes.
            match = re.match(r'(?:0[xX][0-9a-fA-F]+|(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)[i]?', source[i:])
            if not match:
                raise ValueError('Unsupported numeric literal')
            i += len(match.group())
            kind = 'number'
        elif start(source[i]):
            i += 1
            while i < len(source) and continuation(source[i]):
                i += 1
            kind = 'identifier'
        else:
            i += 1
            kind = 'space' if source[begin].isspace() else 'punctuation'
        yield kind, begin, i


def go_transform(source, names, imports):
    result = []
    in_import, grouped = False, False
    for kind, begin, end in tokens(source):
        value = source[begin:end]
        if kind == 'identifier' and value == 'import':
            in_import, grouped = True, False
        elif in_import and value == '(':
            grouped = True
        elif in_import and value == ')':
            in_import = False
        elif in_import and kind == 'string':
            path = value[1:-1]
            if path in imports:
                value = value[0] + imports[path] + value[-1]
            if not grouped:
                in_import = False
        elif kind == 'identifier':
            value = names.get(value, value)
        result.append(value)
    return ''.join(result)


def asm_transform(source, names):
    # Go assembly uses middle-dot-prefixed symbols. NASM/C ABI is untouched.
    output = []
    for kind, begin, end in tokens(source):
        value = source[begin:end]
        if kind == 'identifier' and begin and source[begin - 1] == '·':
            value = names.get(value, value)
        output.append(value)
    return ''.join(output)


def paths_transform(source, paths):
    replacements = {k: v for k, v in paths.items() if k != v}
    if not replacements:
        return source
    pattern = re.compile(r'(?<![\w])(?:' + '|'.join(re.escape(k) for k in sorted(replacements, key=lambda p: (-len(p), p))) + r')(?![\w])')
    return pattern.sub(lambda match: replacements[match.group()], source)


def transform(data, kind, names, imports, paths):
    if kind == 'copy':
        return data
    source = data.decode('utf-8')
    if kind == 'go':
        source = go_transform(source, names, imports)
    elif kind == 'asm':
        source = asm_transform(source, names)
    elif kind == 'paths':
        source = paths_transform(source, paths)
    return source.encode('utf-8')


def safe(root, relative):
    path = Path(relative)
    if path.is_absolute() or not path.parts or '..' in path.parts:
        raise ValueError('Unsafe path: ' + relative)
    result = root / path
    for parent in [result] + list(result.parents):
        if parent == root.parent:
            break
        if parent.is_symlink():
            raise ValueError('Symbolic link is not allowed: ' + str(parent))
    return result


def inverse(mapping):
    if len(set(mapping.values())) != len(mapping):
        raise ValueError('Non-injective mapping')
    return {v: k for k, v in mapping.items()}


def local_path(root, relative):
    """Resolve a historical management path through this directory's own map.

    No links or external source trees are followed. The unchanged fallback lets
    old independent packages and newly generated staging trees keep working.
    """
    root = Path(root)
    safe(root, relative)
    registry = safe(root, 'layout.json')
    if not registry.exists():
        return safe(root, relative)
    config = json.loads(registry.read_text(encoding='utf-8'))
    if config.get('version') != 1 or not isinstance(config.get('paths'), dict):
        raise ValueError('Invalid local path registry: ' + str(registry))
    relative = str(relative)
    for old, new in sorted(config['paths'].items(), key=lambda item: -len(item[0])):
        safe(root, old)
        safe(root, new)
        if relative == old or relative.startswith(old + '/'):
            return safe(root, new + relative[len(old):])
    return safe(root, relative)


def stage(tree, destination, manifest):
    names = inverse(manifest['names'])
    imports = inverse(manifest['imports'])
    registered = {entry['native'] for entry in manifest['files']}
    for current, directories, filenames in os.walk(str(tree)):
        if any((Path(current) / name).is_symlink() for name in directories):
            raise ValueError('Symbolic-link directory in native source')
        directories[:] = [name for name in directories if name not in ('build', '.git', '__pycache__')]
        for name in filenames:
            candidate = Path(current) / name
            if candidate.suffix in ('.go', '.s', '.S', '.c', '.h', '.inc', '.ld', '.sh'):
                relative = str(candidate.relative_to(tree))
                if relative not in registered:
                    raise ValueError('Register new source in 문자대응.json before building: ' + relative)
    count = 0
    for entry in manifest['files']:
        data = safe(tree, entry['native']).read_bytes()
        lowered = transform(data, entry['kind'], names, imports, inverse(entry['paths']))
        output = safe(destination, entry['compiler'])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(lowered)
        output.chmod(entry['mode'])
        count += 1
    return count


def verify(tree, manifest):
    if manifest.get('layout_sha256') and hashlib.sha256(safe(tree, 'layout.json').read_bytes()).hexdigest() != manifest['layout_sha256']:
        raise RuntimeError('Local management-path registry has been modified')
    changed = []
    for entry in manifest['files']:
        content = safe(tree, entry['native']).read_bytes()
        if hashlib.sha256(content).hexdigest() != entry['sha256']:
            changed.append(entry['native'])
    if changed:
        raise RuntimeError('Source changed since generation (build still accepts edits): ' + ', '.join(changed))
    if manifest.get('adapter_sha256'):
        adapter = local_path(tree, '문자빌드.py').read_bytes()
        if hashlib.sha256(adapter).hexdigest() != manifest['adapter_sha256']:
            raise RuntimeError('Local build adapter has been modified')
    return len(manifest['files'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', choices=['kernel', 'iso', 'userland', 'verify', 'stage'])
    parser.add_argument('--tree', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    tree = args.tree.resolve()
    manifest = json.loads(local_path(tree, '문자대응.json').read_text(encoding='utf-8'))
    if args.target == 'verify':
        print('PASS', manifest['profile'], verify(tree, manifest), 'source files')
        return
    build = safe(tree, 'build')
    build.mkdir(exist_ok=True)
    # Fresh staging prevents stale objects after edits or profile switches.
    with tempfile.TemporaryDirectory(prefix='native-stage-', dir=str(build)) as temporary:
        destination = Path(temporary)
        stage(tree, destination, manifest)
        if args.target == 'stage':
            print('PASS', manifest['profile'], 'native-to-Go staging')
            return
        directory = destination
        targets = [args.target]
        if args.target == 'userland':
            directory = safe(destination, manifest['userland'])
            targets = ['check', 'test-programs']
        subprocess.check_call(['make', '-B', '-C', str(directory)] + targets)
        output = build / 'userland' if args.target == 'userland' else build
        output.mkdir(exist_ok=True)
        for artifact in (directory / 'build').iterdir():
            if artifact.is_file():
                target = safe(output, artifact.name)
                # Never publish a partially written kernel.
                with tempfile.NamedTemporaryFile(dir=str(output), delete=False) as temporary_output:
                    temporary_path = Path(temporary_output.name)
                try:
                    shutil.copy2(str(artifact), str(temporary_path))
                    os.replace(str(temporary_path), str(target))
                finally:
                    if temporary_path.exists():
                        temporary_path.unlink()
        print('PASS', manifest['profile'], args.target)


if __name__ == '__main__':
    main()
