#!/usr/bin/env python3
"""Bounded kernel fixes required by shell execution, COW and typed file paths.

Preserve local names, verify prior hashes, back up exact files and record the
before/after audit. No kernel regeneration and no blanket textual replacement.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

from install_shells import editions
from generate_script_variants import rows
from native_source import tokens, safe, inverse, transform, local_path, verify as verify_variant
from refine_country_names import verify as verify_country


def sha(data):
    return hashlib.sha256(data).hexdigest()


def function_span(source, name):
    sequence = [(kind, begin, end, source[begin:end]) for kind, begin, end in tokens(source) if kind not in ('space', 'comment')]
    for index, token in enumerate(sequence[:-1]):
        if token[3] != 'func':
            continue
        following = index + 1
        if sequence[following][3] == '(':
            # Methods have a parenthesized receiver before their name.
            following = next(n for n in range(following + 1, len(sequence)) if sequence[n][3] == ')') + 1
        if sequence[following][3] == name:
            opening = next(n for n in range(following + 1, len(sequence)) if sequence[n][3] == '{')
            depth = 0
            for n in range(opening, len(sequence)):
                depth += sequence[n][3] == '{'
                depth -= sequence[n][3] == '}'
                if depth == 0:
                    return sequence[opening][1], sequence[n][2]
    raise ValueError('Missing function: ' + name)


def patch_cow(source, name, reload):
    begin, end = function_span(source, name)
    body = source[begin:end]
    marker = '\n\treturn true\n}'
    if not body.endswith(marker):
        raise ValueError('Unexpected COW helper ending')
    if '\n\t' + reload + '()\n' in body:
        return source
    body = body[:-len(marker)] + '\n\t// Publish the new physical frame before writing through its virtual address.\n\t' + reload + '()' + marker
    return source[:begin] + body + source[end:]


def patch_slash(source, name):
    begin, end = function_span(source, name)
    body = source[begin:end]
    old, new = "case 0x35:\n\t\treturn '-'", "case 0x35:\n\t\treturn '/'"
    if new in body:
        return source
    if body.count(old) != 1:
        raise ValueError('Unexpected polled keyboard slash mapping')
    return source[:begin] + body.replace(old, new) + source[end:]


def patch_aligned(source, names):
    begin, end = function_span(source, names['AlignedMalloc'])
    canonical = Path(__file__).with_name('aligned_allocator_body.go.in').read_bytes().rstrip()
    body = transform(canonical, 'go', names, {}, {}).decode('utf-8')
    return source[:begin] + body + source[end:]


def apply(root, record, backup_root):
    edition, parent, _ = record
    tree = local_path(parent, '소스')
    is_variant = local_path(tree, '문자대응.json').is_file()
    audit_path = local_path(tree, '문자대응.json' if is_variant else '명명검증.json')
    audit = json.loads(audit_path.read_text(encoding='utf-8'))
    if is_variant:
        verify_variant(tree, audit)
        names = {row[0]: row[2] for row in rows(local_path(tree, '식별자대응.tsv'))[1:]}
    else:
        verify_country(tree)
        names = {row[0]: row[1] for row in rows(local_path(tree, '이름대응표.tsv'))[1:]}
    paths = dict(rows(local_path(tree, '파일대응표.tsv'))[1:])
    changes = {}
    for original, rewrite in [
        ('src/paging/paging.go', lambda text: patch_cow(text, names['makePagePrivateWritableCurrent'], names['reloadCR3'])),
        ('src/systemcall/systemcall.go', lambda text: patch_slash(text, names['scancodeToByte'])),
        ('src/memorymanager/memorymanager.go', lambda text: patch_aligned(text, names))]:
        relative = paths[original]
        before = safe(tree, relative).read_bytes()
        after = rewrite(before.decode('utf-8')).encode('utf-8')
        if before != after:
            changes[relative] = (before, after)
    if not changes:
        print('UNCHANGED', edition, flush=True)
        return
    destination = backup_root / edition
    destination.mkdir(parents=True)
    shutil.copy2(str(audit_path), str(destination / audit_path.name))
    for relative, (before, _) in changes.items():
        output = safe(destination, relative)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(before)
    audit_before = sha(audit_path.read_bytes())
    # Check all snapshots immediately before the bounded write set.
    for relative, (before, _) in changes.items():
        if safe(tree, relative).read_bytes() != before:
            raise ValueError('Source changed during planning: ' + relative)
    for relative, (_, after) in changes.items():
        safe(tree, relative).write_bytes(after)
        if is_variant:
            entry = next(entry for entry in audit['files'] if entry['native'] == relative)
            entry['sha256'] = sha(after)
            restored = transform(after, entry['kind'], inverse(audit['names']), inverse(audit['imports']), inverse(entry['paths']))
            entry['compiler_sha256'] = sha(restored)
        else:
            audit['hashes'][relative] = sha(after)
    audit.setdefault('functional_fixes', {})['shell-kernel-paths-v2'] = {
        'prior_audit_sha256': audit_before, 'backup': str(destination),
        'files': {relative: {'before': sha(before), 'after': sha(after)} for relative, (before, after) in changes.items()}}
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('FIXED', edition, len(changes), 'files', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', action='append', default=[])
    args = parser.parse_args()
    records = editions(args.root)
    if set(args.edition) - {record[0] for record in records}:
        parser.error('unknown edition')
    backup = Path(tempfile.mkdtemp(prefix='worldos-shell-kernel-backup-'))
    print('Backup:', backup, flush=True)
    for record in records:
        if not args.edition or record[0] in args.edition:
            apply(args.root, record, backup)


if __name__ == '__main__':
    main()
