"""Pure, auditable metadata-path translation, also used on generator staging trees."""
import csv
import hashlib
import io
import json
from pathlib import Path

from layout_terms import KEYS, proposals
from native_source import inverse, transform


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def checksum(data):
    return hashlib.sha256(data).hexdigest()


def remap(relative, mapping):
    for old, new in sorted(mapping.items(), key=lambda item: -len(item[0])):
        if relative == old or relative.startswith(old + '/'):
            return new + relative[len(old):]
    return relative


def translate(initial, language):
    """Return (new file bytes/modes, exact renames, registry), without writes.

    Executable/compiler source is unchanged except reversible management-path
    references. Existing hash dictionaries are relocated, never discarded.
    """
    desired, status = proposals(language)
    source_directory = desired.pop('소스')  # The edition root owns this directory.
    for name in KEYS:
        if name not in ('소스', '원본자료'):
            desired['원본자료/' + name] = desired['원본자료'] + '/' + desired[name]
    current = json.loads(initial['layout.json'][0].decode('utf-8'))['paths'] if 'layout.json' in initial else {}
    moves = {current.get(old, old): new for old, new in desired.items()}
    paths = {old: remap(old, moves) for old in initial}
    if len(set(paths.values())) != len(paths):
        raise ValueError('Existing file collides with a proposed management path')
    final = {paths[old]: value for old, value in initial.items()}
    registry = {'version': 1, 'language': language, 'status': status, 'paths': desired,
                'scope': 'edition-local management names; compiler syntax and file formats unchanged'}
    final['layout.json'] = (encoded(registry), 0o644)
    # Adjust current path tables, not their canonical/original-name column.
    for legacy in ('파일대응표.tsv', '파일대응.tsv'):
        name = desired[legacy]
        if name in final:
            values = list(csv.reader(io.StringIO(final[name][0].decode('utf-8')), delimiter='\t'))
            for row in values[1:]:
                if len(row) == 2:
                    row[1] = remap(row[1], moves)
            output = io.StringIO()
            writer = csv.writer(output, delimiter='\t', lineterminator='\n')
            writer.writerows(values)
            final[name] = (output.getvalue().encode('utf-8'), final[name][1])
    # Only the active guide/README, never inherited historical documentation.
    for name in ('README.md', desired['문자판안내.md']):
        if name in final:
            data = final[name][0].decode('utf-8')
            data = data.replace('../소스', '../' + source_directory)
            for old, new in sorted(moves.items(), key=lambda item: -len(item[0])):
                if Path(old).suffix:
                    data = data.replace(old, new)
            final[name] = (data.encode('utf-8'), final[name][1])
    if desired['문자대응.json'] in final:
        name = desired['문자대응.json']
        manifest = json.loads(final[name][0].decode('utf-8'))
        for entry in manifest['files']:
            old = entry['native']
            entry['native'] = remap(old, moves)
            # Lower before updating path rules, then apply the new rules. This
            # proves that changing build-rules.mk cannot alter compiler input.
            data = initial[old][0]
            lowered = transform(data, entry['kind'], inverse(manifest['names']), inverse(manifest['imports']), inverse(entry['paths']))
            if checksum(lowered) != entry['compiler_sha256']:
                raise ValueError('Pre-migration compiler input differs: ' + old)
            entry['paths'] = {key: remap(value, moves) for key, value in entry['paths'].items()}
            updated = transform(lowered, entry['kind'], manifest['names'], manifest['imports'], entry['paths'])
            final[entry['native']] = (updated, final[entry['native']][1])
            entry['sha256'] = checksum(updated)
        adapter_old = current.get('문자빌드.py', '문자빌드.py')
        adapter_new = desired['문자빌드.py']
        manifest['adapter_sha256'] = checksum(final[adapter_new][0])
        make, mode = final['Makefile']
        final['Makefile'] = (make.decode('utf-8').replace(adapter_old, adapter_new).encode('utf-8'), mode)
        manifest['layout_sha256'] = checksum(final['layout.json'][0])
        final[name] = (encoded(manifest), final[name][1])
    for name in ('posix.json', 'shell.json', desired['명명검증.json']):
        if name not in final:
            continue
        config = json.loads(final[name][0].decode('utf-8'))
        config['hashes'] = {remap(old, moves): checksum(final[remap(old, moves)][0]) for old in config['hashes']}
        config['hashes']['layout.json'] = checksum(final['layout.json'][0])
        final[name] = (encoded(config), final[name][1])
    return final, {old: new for old, new in paths.items() if old != new}, registry


def localize_stage(tree, language):
    """Translate a generator-owned staging tree before its outer publication."""
    initial = {str(path.relative_to(tree)): (path.read_bytes(), path.stat().st_mode & 0o777)
               for path in tree.rglob('*') if path.is_file()}
    final, moves, _ = translate(initial, language)
    # No files leave staging. The caller owns its cleanup and atomic publication.
    for old, new in sorted(moves.items(), key=lambda item: -len(item[0])):
        target = tree / new
        target.parent.mkdir(parents=True, exist_ok=True)
        (tree / old).rename(target)
    for name, (data, mode) in final.items():
        path = tree / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(mode)
    return final
