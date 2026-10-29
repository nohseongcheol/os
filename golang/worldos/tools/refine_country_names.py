#!/usr/bin/env python3
"""Auditable, token-only naming migration of existing independent WorldOS trees.

Default is a dry run. Never regenerate a country's implementation from engos.
Only whole, explicit concepts get new translations. Uncovered terms stay visible.
"""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unicodedata

from naming_lexicon import lexicon, IDENTIFIERS, PACKAGES, RATIONALE
from native_source import local_path

VERSION = 'function-meaning-v1'
FIXED = set('main init KKernelEntry _ Data Len Cap Pointer Sizeof Offsetof Alignof'.split())
LEXICON = lexicon()


def rows(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.reader(stream, delimiter='\t'))


def tsv(header, values):
    output = io.StringIO()
    writer = csv.writer(output, delimiter='\t', lineterminator='\n')
    writer.writerow(header)
    writer.writerows(values)
    return output.getvalue().encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identifier(phrase, exported=False, role='', typed=False):
    value = unicodedata.normalize('NFC', phrase).replace(' ', '_').replace('-', '_')
    # Unicode modifier apostrophe is a letter in Go; do not strip script marks.
    if not value or not all(ch == '_' or unicodedata.category(ch).startswith('L') or
                            unicodedata.category(ch) == 'Nd' for ch in value):
        raise ValueError('Go cannot represent this phrase without a reviewed spelling: ' + phrase)
    value = value[0].upper() + value[1:] if exported else value[0].lower() + value[1:]
    if typed and role in ('T', 'I'):
        value = role + value
    elif exported and not value[0].isupper():
        value = (role or 'V') + value
    return value


def files_in(tree):
    for current, dirs, files in os.walk(str(tree)):
        dirs[:] = sorted(d for d in dirs if d not in ('build', '.git', '__pycache__'))
        for name in sorted(files):
            path = Path(current) / name
            if path.is_symlink():
                raise RuntimeError('Refusing symbolic link: ' + str(path))
            yield path


def phrase(language, concept):
    if language == 'und':
        return LEXICON['en'][concept], 'undefined-language-English'
    local = LEXICON.get(language, {}).get(concept)
    return (local or LEXICON['en'][concept],
            'project-proposal' if local else 'pending-language-review')


def korean_names(root):
    values = {}
    for original, target, _ in rows(root / '명명/ko-식별자.tsv')[1:]:
        values.setdefault(original, set()).add(target)
    # Different meanings of the same spelling require scoped rules, not a guess.
    return {key: next(iter(value)) for key, value in values.items() if len(value) == 1}


def safe_join(tree, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise RuntimeError('Unsafe mapped path: ' + relative)
    return tree / path


def path_substitution(text, replacements):
    replacements = {k: v for k, v in replacements.items() if k != v}
    if not replacements:
        return text
    # One pass, whole path boundaries: never change nasm, go_asm.h or build IDs.
    pattern = re.compile(r'(?<![\w])(?:' + '|'.join(re.escape(k) for k in
                          sorted(replacements, key=lambda x: (-len(x), x))) + r')(?![\w])')
    return pattern.sub(lambda match: replacements[match.group(0)], text)


def prepare(tree, language, root, token_tool):
    original_names = rows(local_path(tree, '이름대응표.tsv'))[1:]
    original_paths = rows(local_path(tree, '파일대응표.tsv'))[1:]
    initial = {str(p.relative_to(tree)): (p.read_bytes(), p.stat().st_mode & 0o777)
               for p in files_in(tree)}
    mapping = {}
    details = {}
    korean = korean_names(root) if language == 'ko' else {}
    for original, current, *_ in original_names:
        candidate = current
        status, concept = 'existing-unreviewed', ''
        if original in FIXED or current in FIXED:
            status = 'compatibility'
        elif original in korean:
            candidate = korean[original]
            status = 'koros4-function-reviewed'
        elif original in IDENTIFIERS:
            concept, role = IDENTIFIERS[original]
            translated, status = phrase(language, concept)
            # Never replace an existing native word by English just because the
            # new lexicon is incomplete. Only proven misleading names require
            # a functional correction even while translation remains pending.
            if status != 'pending-language-review' or original in ('PushBack', 'PushFront', 'PushAt', 'UnsetBit', 'ModelToScreen'):
                candidate = identifier(translated, current[0].isupper(), role, role in ('T', 'I'))
                if original == 'TBiosParameterBlock32':
                    candidate += '32'
        mapping[current] = candidate
        details[original] = [current, candidate, status, concept]

    # Package aliases are changed together with their exact import path.
    # The legacy mouse source incorrectly declares `package keyboard`; do not
    # globally rename keyboard. Its directory is still safe to localize.
    for package, concept in PACKAGES.items():
        original = package.rsplit('/', 1)[-1]
        if original in details and original != 'mouse':
            text, status = phrase(language, concept)
            if status == 'pending-language-review':
                continue
            target = identifier(text)
            current = details[original][0]
            mapping[current] = target
            details[original] = [current, target, status, concept]

    # Reserve untouched names first. Preserve distinct declarations rather than
    # accidentally merging them because two concepts share a translation.
    used = {value: key for key, value in mapping.items() if key == value}
    for current in sorted(mapping):
        candidate = mapping[current]
        if candidate in used and used[candidate] != current:
            base = candidate
            for number in range(2, len(mapping) + 2):
                candidate = base + '_' + str(number)
                if candidate not in used:
                    break
        used[candidate] = current
        mapping[current] = candidate
    for original, detail in details.items():
        detail[1] = mapping[detail[0]]
    if len(set(mapping.values())) != len(mapping):
        raise RuntimeError('Non-injective identifier map')

    paths = {old: old for old in initial}
    canonical = {original: current for original, current in original_paths}
    korean_paths = dict(rows(root / '명명/ko-경로.tsv')[1:]) if language == 'ko' else {}
    imports = {}
    package_destinations = {}
    for original, current in original_paths:
        target = korean_paths.get(original, current)
        if original.startswith('src/') and language != 'ko':
            original_dir = str(Path(original).parent)[4:]
            if original_dir in PACKAGES and phrase(language, PACKAGES[original_dir])[1] != 'pending-language-review':
                stem = identifier(phrase(language, PACKAGES[original_dir])[0])
                parent = str(Path(current).parent.parent)
                directory = parent + '/' + stem
                filename = Path(current).name
                if Path(original).stem == Path(original_dir).name:
                    filename = stem + Path(original).suffix
                target = directory + '/' + filename
        paths[current] = target
        if original.startswith('src/'):
            old_import = str(Path(current).parent)[4:]
            new_import = str(Path(target).parent)[4:]
            if old_import in imports and imports[old_import] != new_import:
                raise RuntimeError('Inconsistent package path')
            imports[old_import] = new_import
            package_destinations[str(Path(original).parent)] = str(Path(target).parent)

    def term(concept):
        return identifier(phrase(language, concept)[0])

    # Root build contracts remain Makefile, src and build. The compiler script,
    # linker script and helper paths are private and can be renamed safely.
    root_paths = {'go.sh': term('compile_kernel') + '.sh',
                  'linker.ld': term('link_layout') + '.ld'}
    paths.update({p: q for p, q in root_paths.items() if p in initial})
    asm_dir, tools_dir = term('boot'), term('tools')
    user_dir = term('user_space') + '/posix'
    for old in initial:
        if old.startswith('asm/'):
            paths[old] = asm_dir + '/' + Path(paths[old]).name
        elif old.startswith('tools/'):
            name = {'offsets.go': term('structure_offsets') + '.go',
                    'decode-virtualbox-log.sh': term('log_decoder') + '.sh'}.get(Path(old).name, Path(old).name)
            paths[old] = tools_dir + '/' + name
        elif old.startswith('userland/posix/'):
            tail = old[len('userland/posix/'):]
            subdirs = {'src': term('implementation'), 'tests': term('tests'), 'include': term('headers')}
            parts = tail.split('/')
            parts[0] = subdirs.get(parts[0], parts[0])
            if tail == 'linker.ld':
                parts[-1] = term('link_layout') + '.ld'
            elif tail.startswith('src/'):
                concepts = {'syscall.S': 'system_call', 'crt0.S': 'startup', 'errno.c': 'error_number',
                            'fcntl.c': 'file_control', 'stat.c': 'file_status'}
                if Path(old).name in concepts:
                    parts[-1] = term(concepts[Path(old).name]) + Path(old).suffix
            paths[old] = user_dir + '/' + '/'.join(parts)

    if len(set(paths.values())) != len(paths):
        raise RuntimeError('File path collision: ' + str(tree))
    for target in paths.values():
        safe_join(tree, target)
    kernel_files = [str(tree / current) for original, current in original_paths if original.endswith('.go')]
    payload = {'Files': kernel_files, 'Names': mapping, 'Imports': imports}
    process = subprocess.run([str(token_tool)], input=json.dumps(payload).encode(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode:
        raise RuntimeError(process.stderr.decode('utf-8', 'replace'))
    changed_tokens = 0
    counts = {}
    output = dict(initial)
    for line in process.stdout.decode().splitlines():
        item = json.loads(line)
        relative = str(Path(item['Path']).relative_to(tree))
        output[relative] = (item['Source'].encode(), initial[relative][1])
        changed_tokens += item['Replacements']
        for key, value in item['Counts'].items():
            counts[key] = counts.get(key, 0) + value

    assembly_pattern = re.compile(r'·([^\W\d]\w*)', re.UNICODE)
    all_paths = {old: new for old, new in paths.items() if old != new}
    # Used in root Makefile and documentation, always as complete paths.
    all_paths.update({'asm/': asm_dir + '/', 'tools/': tools_dir + '/',
                      'userland/posix/': user_dir + '/'})
    all_paths.update({'userland/posix/include': user_dir + '/' + term('headers'),
                      'userland/posix/src': user_dir + '/' + term('implementation'),
                      'userland/posix/tests': user_dir + '/' + term('tests'),
                      'userland/posix': user_dir})
    for old, (data, mode) in list(output.items()):
        suffix = Path(old).suffix
        if suffix in ('.c', '.h', '.S') or old.endswith('.go'):
            continue
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            continue
        if suffix == '.s' and not old.startswith('asm/'):
            text = assembly_pattern.sub(lambda match: '·' + mapping.get(match.group(1), match.group(1)), text)
        if old in ('Makefile', 'go.sh', 'DEBUGGING.md', 'POSIX.md', 'readme.txt', 'README.md') or old.startswith('asm/'):
            text = path_substitution(text, all_paths)
        if old.startswith('asm/'):
            text = path_substitution(text, {Path(key).name: Path(value).name for key, value in paths.items()
                                            if key.startswith('asm/')})
        if old == 'userland/posix/Makefile':
            relative_paths = {key[len('userland/posix/'):]: value[len(user_dir) + 1:]
                              for key, value in paths.items() if key.startswith('userland/posix/')}
            # Expand the C pattern rule before renaming filenames so object/ABI
            # names remain unchanged even though implementation files move.
            pattern_rule = '$(BUILD)/%.o: src/%.c | $(BUILD)\n\t$(CC) $(CFLAGS) -c $< -o $@'
            explicit = '\n\n'.join('$(BUILD)/{0}.o: src/{0}.c | $(BUILD)\n\t$(CC) $(CFLAGS) -c $< -o $@'.format(name)
                                   for name in ('errno', 'unistd', 'fcntl', 'stat', 'socket'))
            if pattern_rule not in text:
                raise RuntimeError('Unexpected C pattern rule in ' + str(tree))
            text = text.replace(pattern_rule, explicit)
            relative_paths['-Iinclude'] = '-I' + term('headers')
            text = path_substitution(text, relative_paths)
        output[old] = (text.encode(), mode)

    # All project C implementation and public-header bytes remain identical.
    for old, (data, _) in initial.items():
        if Path(old).suffix in ('.c', '.h', '.S') and output[old][0] != data:
            raise RuntimeError('Unexpected C/ABI edit: ' + old)
    final = {paths[old]: value for old, value in output.items()}
    name_rows = [[original, details[original][1], language] for original, *_ in original_names]
    final['이름대응표.tsv'] = (tsv(['original', 'localized', 'language'], name_rows), 0o644)
    # Extend the original map to cover private scripts and C source paths too.
    path_rows = [[original, paths[current]] for original, current in original_paths]
    represented = {current for _, current in original_paths}
    path_rows += [[old, paths[old]] for old in sorted(initial) if old not in represented and
                  (old in root_paths or old.startswith(('tools/', 'userland/posix/')))]
    final['파일대응표.tsv'] = (tsv(['원래경로', '변환경로'], path_rows), 0o644)
    report_rows = [[original] + details[original] + [counts.get(details[original][0], 0)] for original, *_ in original_names]
    final['새명명-식별자.tsv'] = (tsv(['original', 'before', 'after', 'review_status', 'concept', 'changed_tokens'], report_rows), 0o644)
    final['새명명-경로.tsv'] = (tsv(['before', 'after'], [[old, paths[old]] for old in sorted(paths) if old != paths[old]]), 0o644)
    terms, pending = [], []
    for concept in sorted(LEXICON['en']):
        text, status = phrase(language, concept)
        terms.append([concept, text, identifier(text), status, RATIONALE.get(concept, 'function-based project proposal')])
        if status.startswith('pending'):
            pending.append(['concept', concept, 'missing whole-phrase translation; English is not a native-language translation'])
    for original, detail in sorted(details.items()):
        if detail[2] in ('existing-unreviewed', 'pending-language-review'):
            pending.append(['identifier', original, 'existing spelling retained; current-function and linguistic review incomplete'])
    final['새명명-용어.tsv'] = (tsv(['concept', 'native_phrase_or_english_fallback', 'code_spelling', 'status', 'rationale'], terms), 0o644)
    final['명명검토대기.tsv'] = (tsv(['kind', 'original', 'reason'], pending), 0o644)
    summary = {'country': tree.parent.name, 'language': language, 'version': VERSION,
               'language_fallback': 'en' if language == 'und' else '',
               'identifiers_changed': sum(a != b for a, b in mapping.items()),
               'identifier_tokens_changed': changed_tokens,
               'paths_changed': sum(a != b for a, b in paths.items()),
               'native_concept_proposals': sum(row[3] == 'project-proposal' for row in terms),
               'pending_concepts': sum(row[3].startswith('pending') for row in terms),
               'unreviewed_identifiers': sum(row[0] == 'identifier' for row in pending),
               'kernel_go_files_token_checked': len(kernel_files),
               'c_abi_bytes_unchanged': True, 'linguistic_review_complete': False}
    readme_note = ('\n## 기능·어원 중심 명명 개정\n\n'
                   '현재 기능에 따른 전체 표현은 `새명명-용어.tsv`, 식별자와 경로 변경은 '
                   '`새명명-식별자.tsv`, `새명명-경로.tsv`에 기록합니다. '
                   '이 표현은 WorldOS 프로젝트 제안이며 공인 표준 번역이나 원어민 감수 완료를 뜻하지 않습니다. '
                   '미검토 항목은 `명명검토대기.tsv`에 남겼습니다. '
                   '영어 대체 이름은 해당 언어의 번역으로 집계하지 않습니다. '
                   'C 공개 ABI·헤더 이름·기계 명령·Go 예약어는 유지합니다.\n')
    for name in ('README.md', '나라언어.md'):
        if name in final:
            final[name] = (final[name][0] + readme_note.encode(), final[name][1])
    summary['hashes'] = {name: digest(data) for name, (data, _) in final.items()}
    final['명명검증.json'] = ((json.dumps(summary, ensure_ascii=False, indent=2) + '\n').encode(), 0o644)
    return initial, final, summary


def commit(tree, initial, final):
    # Refuse to overwrite concurrent edits or unexpected targets.
    for old, (data, _) in initial.items():
        if (tree / old).read_bytes() != data:
            raise RuntimeError('Source changed while planning: ' + str(tree / old))
    for new in final:
        if new not in initial and (tree / new).exists():
            raise RuntimeError('Destination exists: ' + str(tree / new))
    with tempfile.TemporaryDirectory(prefix='.naming-stage-', dir=str(tree.parent)) as staging:
        stage = Path(staging)
        for name, (data, mode) in final.items():
            target = safe_join(stage, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            target.chmod(mode)
        for name in sorted(final):
            target = safe_join(tree, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(str(stage / name), str(target))
        # Only exact former paths absent from the new tree are removed.
        for old in sorted(set(initial) - set(final)):
            (tree / old).unlink()
    for current, _, _ in os.walk(str(tree), topdown=False):
        path = Path(current)
        if path != tree and 'build' not in path.relative_to(tree).parts:
            try:
                path.rmdir()
            except OSError:
                pass


def verify(tree):
    summary = json.loads(local_path(tree, '명명검증.json').read_text(encoding='utf-8'))
    if summary['version'] != VERSION:
        raise RuntimeError('Naming policy changed; review the existing source before migrating again: ' + str(tree))
    for name, expected in summary['hashes'].items():
        if digest(safe_join(tree, name).read_bytes()) != expected:
            raise RuntimeError('File changed since naming audit: ' + str(tree / name))
    for _, target in rows(local_path(tree, '파일대응표.tsv'))[1:]:
        if not safe_join(tree, target).is_file():
            raise RuntimeError('Mapped file missing: ' + target)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--country', action='append', help='ISO alpha-3; default all existing countries')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    countries = sorted(args.country or [p.name for p in (root / '나라').iterdir() if p.is_dir()])
    reports = []
    with tempfile.TemporaryDirectory(prefix='worldos-naming-tool-') as temporary:
        token_tool = Path(temporary) / 'tokens'
        if not args.check:
            subprocess.check_call(['go', 'build', '-o', str(token_tool), str(root / 'tools/naming_tokens.go')])
        for code in countries:
            if not re.match(r'^[A-Z]{3}$', code):
                raise RuntimeError('Invalid country code: ' + code)
            tree = local_path(root / '나라' / code, '소스')
            language = re.search(r'^- selected language: (.+)$', local_path(tree, '나라언어.md').read_text(encoding='utf-8'), re.M).group(1)
            if args.check or local_path(tree, '명명검증.json').exists():
                summary = verify(tree)
            else:
                initial, final, summary = prepare(tree, language, root, token_tool)
                if args.apply:
                    commit(tree, initial, final)
                    verify(tree)
            reports.append(summary)
            print('{country}/{language}: names={identifiers_changed}, tokens={identifier_tokens_changed}, paths={paths_changed}, pending concepts={pending_concepts}'.format(**summary), flush=True)
    if (args.apply or args.check) and not args.country:
        keys = ['country', 'language', 'identifiers_changed', 'identifier_tokens_changed', 'paths_changed',
                'native_concept_proposals', 'pending_concepts', 'unreviewed_identifiers', 'kernel_go_files_token_checked']
        (root / '명명-적용현황.tsv').write_bytes(tsv(keys, [[s[k] for k in keys] for s in reports]))
        terms = [[language, concept, value] for language, concepts in sorted(LEXICON.items())
                 for concept, value in sorted(concepts.items())]
        (root / '명명/언어별표현.tsv').write_bytes(tsv(['language', 'concept', 'project_proposal'], terms))
    print('countries={}, languages={}, mode={}'.format(len(reports), len(set(s['language'] for s in reports)),
                                                     'check' if args.check else 'apply' if args.apply else 'dry-run'))


if __name__ == '__main__':
    main()
