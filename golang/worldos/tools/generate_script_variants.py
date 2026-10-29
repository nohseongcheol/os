#!/usr/bin/env python3
"""Add independent script editions; never overwrite existing country sources.

Terminology is explicitly a proposal, with untranslated identifiers enumerated.
Japanese kana conversion requires generation-only pykakasi 2.0.8 resources.
Building an edition requires only Python stdlib and the existing OS toolchain.
"""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unicodedata

from native_source import inverse, transform, verify, safe, local_path
from variant_terms import INDIA, LIMITED, EXACT, PATH_CONCEPTS, terms, whole_names

FIXED = set('main init KKernelEntry _ Data Len Cap Pointer Sizeof Offsetof Alignof'.split())
SKIP = set('이름대응표.tsv 파일대응표.tsv 새명명-식별자.tsv 새명명-경로.tsv 새명명-용어.tsv 명명검토대기.tsv 명명검증.json'.split())
CYRILLIC = dict(zip('АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ',
                    'A B V G D Đ E Ž Z I J K L Lj M N Nj O P R S T Ć U F H C Č Dž Š'.split()))
CYRILLIC.update({k.lower(): v.lower() for k, v in list(CYRILLIC.items())})
INHERITED_METADATA = {'나라언어.md', '용어사전.tsv', '용어근거.tsv', 'README.md', 'readme.txt', 'DEBUGGING.md', 'POSIX.md'}
INITIAL_ADAPTER_SHA256 = '3f7621f7bb2d0cbfc215e7c333f65b5201c8ae1d5abee1ab8d9834ac12885dde'


def rows(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.reader(stream, delimiter='\t'))


def table(header, values):
    output = io.StringIO()
    writer = csv.writer(output, delimiter='\t', lineterminator='\n')
    writer.writerow(header)
    writer.writerows(values)
    return output.getvalue()


def profiles():
    result = []
    for language, iso, label, script in INDIA:
        result.append(('IND', language + '_' + script, iso, label, 'IND'))
    existing = {p[1] for p in result}
    for profile in sorted(set(LIMITED) - existing):
        language = profile.split('_')[0]
        _, iso, label, _ = next(item for item in INDIA if item[0] == language)
        result.append(('IND', profile, iso, label, 'IND'))
    result += [('JPN', 'ja_' + script, 'jpn', '日本語', 'JPN') for script in ('Jpan', 'Hira', 'Kana')]
    for country in ('CHN', 'HKG', 'MAC', 'TWN'):
        result += [(country, 'zh_' + script, 'zho', '中文', 'CHN' if script == 'Hans' else 'TWN') for script in ('Hans', 'Hant')]
    for country, language, label, base in [('SRB', 'sr', 'српски', 'SRB'), ('MNE', 'sr', 'српски', 'SRB'), ('BIH', 'bs', 'bosanski', 'BIH')]:
        result += [(country, language + '_' + script, 'srp' if language == 'sr' else 'bos', label, base) for script in ('Cyrl', 'Latn')]
    return result


def label_name(value, original):
    result = unicodedata.normalize('NFC', value).replace(' ', '_')
    # Prefix carries exported/type distinction through an uncased script.
    if original[:1].isupper():
        result = ('T' if original.startswith('T') else 'V') + result
    if not result or len(result.encode('utf-8')) > 230:
        raise ValueError('Invalid or overlong proposed name: ' + original)
    return result


def all_files(tree):
    skipped = {str(local_path(tree, name).relative_to(tree)) for name in SKIP} | {'layout.json'}
    inherited = {str(local_path(tree, name).relative_to(tree)): name for name in INHERITED_METADATA}
    for current, dirs, files in os.walk(str(tree)):
        if any((Path(current) / directory).is_symlink() for directory in dirs):
            raise ValueError('Symbolic-link directory in source: ' + current)
        dirs[:] = sorted(d for d in dirs if d not in ('build', '.git', '__pycache__', 'iso'))
        for filename in sorted(files):
            path = Path(current) / filename
            if path.is_symlink():
                raise ValueError('Cannot clone symbolic link: ' + str(path))
            relative = str(path.relative_to(tree))
            if relative not in skipped:
                yield inherited.get(relative, relative), path


def japanese_converter(resources, script):
    sys.path.insert(0, str(resources / 'python'))
    from pykakasi import kakasi
    reader = kakasi()
    mode = 'hira' if script == 'Hira' else 'kana'
    # Context-dependent compounds need explicit readings, not isolated kanji.
    readings = {'共有媒体網伝送枠': 'きょうゆうばいたいもうでんそうわく',
                '共有媒体網': 'きょうゆうばいたいもう', '広域相互接続網': 'こういきそうごせつぞくもう'}
    cache = {}
    def convert(value):
        if value not in cache:
            output = []
            for chunk in re.split(r'([\u3040-\u30ff\u3400-\u9fff]+)', value):
                if not re.search(r'[\u3040-\u30ff\u3400-\u9fff]', chunk):
                    output.append(chunk)  # Never phoneticize uncovered English.
                else:
                    reading = readings.get(chunk)
                    if reading:
                        output.append(reading if mode == 'hira' else ''.join(chr(ord(c) + 96) if '\u3041' <= c <= '\u3096' else c for c in reading))
                    else:
                        output.append(''.join(part[mode] for part in reader.convert(chunk)))
            cache[value] = ''.join(output)
        return cache[value]
    return convert


def path_rules(files, relative):
    """Per-file path context; C make paths are relative to its own directory."""
    base = str(Path(relative).parent)
    pairs = files
    if Path(relative).name == 'Makefile' and base != '.':
        target_base = str(Path(files[relative]).parent)
        pairs = {old[len(base) + 1:]: new[len(target_base) + 1:] for old, new in files.items()
                 if old.startswith(base + '/') and new.startswith(target_base + '/')}
    rules = {}
    for old, new in pairs.items():
        rules[old] = new
        old_parts, new_parts = Path(old).parts, Path(new).parts
        if len(old_parts) == len(new_parts):
            for index in range(1, len(old_parts)):
                rules['/'.join(old_parts[:index])] = '/'.join(new_parts[:index])
    # NASM %include uses bare sibling names, not paths from project root.
    if relative.endswith(('.inc', '.s')) and '·' not in relative:
        for old, new in files.items():
            if str(Path(old).parent) == base:
                rules[Path(old).name] = Path(new).name
    rules = {k: v for k, v in rules.items() if k != v}
    inverse(rules)
    return rules


def generate(root, record, resources):
    country, profile, iso, native_label, lexical_country = record
    donor = local_path(root / '나라' / country, '소스')
    lex = local_path(root / '나라' / lexical_country, '소스')
    destination = local_path(root / '문자판' / country / profile, '소스')
    if destination.exists():
        manifest = json.loads(local_path(destination, '문자대응.json').read_text(encoding='utf-8'))
        verify(destination, manifest)
        # Move only intact generator-owned provenance, never user-edited files.
        # These describe the donor language, not this edition's translation.
        repaired = manifest['iso639_3'] != iso
        manifest['iso639_3'] = iso
        manifest['summary']['iso639_3'] = iso
        adapter = local_path(destination, '문자빌드.py')
        expected = manifest.get('adapter_sha256', INITIAL_ADAPTER_SHA256)
        if hashlib.sha256(adapter.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Refusing to replace edited build adapter: ' + str(adapter))
        adapter_data = (root / 'tools/native_source.py').read_bytes()
        adapter_hash = hashlib.sha256(adapter_data).hexdigest()
        if manifest.get('adapter_sha256') != adapter_hash:
            adapter.write_bytes(adapter_data)
            manifest['adapter_sha256'] = adapter_hash
            repaired = True
        for entry in manifest['files']:
            if entry['native'] in INHERITED_METADATA:
                old = safe(destination, entry['native'])
                entry['native'] = str(local_path(destination, '원본자료/' + entry['native']).relative_to(destination))
                target = safe(destination, entry['native'])
                target.parent.mkdir(exist_ok=True)
                if target.exists():
                    raise RuntimeError('Provenance destination already exists')
                old.rename(target)
                repaired = True
        if repaired:
            local_path(destination, '문자대응.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return manifest['summary']
    lexical_names = {original: localized for original, localized, _ in rows(local_path(lex, '이름대응표.tsv'))[1:]}
    canonical_paths = dict(rows(local_path(donor, '파일대응표.tsv'))[1:])
    lexical_paths = dict(rows(local_path(lex, '파일대응표.tsv'))[1:])
    reverse_paths = inverse(canonical_paths)
    source_files = dict(all_files(donor))
    vocabulary, phrases = terms(profile), whole_names(profile)
    convert = lambda value: value
    script = profile.split('_')[1]
    if profile in ('ja_Hira', 'ja_Kana'):
        convert = japanese_converter(resources, script)
    elif profile in ('sr_Latn', 'bs_Latn'):
        convert = lambda value: ''.join(CYRILLIC.get(ch, ch) for ch in value)
    names, details = {}, []
    used = set(FIXED)
    original_names = rows(local_path(donor, '이름대응표.tsv'))[1:]
    # Reserve compatibility identifiers and avoid global name collisions.
    for original, current, _ in original_names:
        if original in FIXED or current in FIXED:
            names[current] = current
    for original, current, _ in original_names:
        status = 'existing-unreviewed'
        if current in names:
            candidate, status = current, 'compatibility'
        elif country == 'IND':
            phrase = phrases.get(original) or vocabulary.get(EXACT.get(original, ''))
            candidate = label_name(phrase, original) if phrase else original
            status = 'project-proposal' if phrase else 'pending-translation'
        else:
            candidate = convert(lexical_names.get(original, current))
            if profile in ('ja_Hira', 'ja_Kana'):
                status = 'reading-needs-review'
        if current not in names:
            base, number = candidate, 2
            while candidate in used:
                candidate = base + '_' + str(number)
                number += 1
            names[current] = candidate
            used.add(candidate)
        details.append([original, current, candidate, status])
    inverse(names)
    paths = {}
    for current in source_files:
        original = reverse_paths.get(current, current)
        if country == 'IND':
            # Keep unreviewed implementation names visible; no Hindi fallback.
            parts = []
            for part in Path(original).parts:
                stem, suffix = os.path.splitext(part)
                concept = PATH_CONCEPTS.get(stem)
                parts.append((unicodedata.normalize('NFC', vocabulary[concept]).replace(' ', '_') if concept in vocabulary else stem) + suffix)
            target = '/'.join(parts)
        else:
            target = convert(lexical_paths.get(original, current))
        if current == 'Makefile':
            target = '빌드규칙.mk'
        elif current in INHERITED_METADATA:
            target = '원본자료/' + current
        safe(destination, target)
        if any(len(part.encode('utf-8')) > 255 for part in Path(target).parts):
            raise ValueError('Filename too long: ' + target)
        paths[current] = target
    inverse(paths)
    imports = {}
    for current, target in paths.items():
        if current.startswith('src/') and current.endswith('.go'):
            imports[str(Path(current).parent)[4:]] = str(Path(target).parent)[4:]
    inverse(imports)
    manifest = {'version': 1, 'profile': profile, 'country': country,
                'iso639_3': iso, 'native_language': native_label, 'script': script,
                'source_dialect': 'WorldOS native identifier dialect; lowered to Go 1.10',
                'names': names, 'imports': imports, 'files': [],
                'userland': str(Path(canonical_paths['userland/posix/Makefile']).parent)}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='variant-generate-') as temporary:
        output = Path(temporary) / 'source'
        output.mkdir()
        for current, source in sorted(source_files.items()):
            data = source.read_bytes()
            kind, rules = 'copy', {}
            if current.endswith('.go') and (current.startswith('src/') or '/' not in current):
                kind = 'go'
            elif current.endswith('.s') and '·'.encode() in data:
                kind = 'asm'
            elif current.endswith(('.s', '.inc', '.sh')) or Path(current).name == 'Makefile':
                try:
                    data.decode('utf-8')
                    kind, rules = 'paths', path_rules(paths, current)
                except UnicodeDecodeError:
                    pass
            native = transform(data, kind, names, imports, rules)
            restored = transform(native, kind, inverse(names), inverse(imports), inverse(rules))
            if restored != data:
                raise RuntimeError('Non-lossless transformation: ' + current + ' in ' + profile)
            target = safe(output, paths[current])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(native)
            target.chmod(source.stat().st_mode & 0o777)
            manifest['files'].append({'native': paths[current], 'compiler': current,
                'kind': kind, 'paths': rules, 'mode': source.stat().st_mode & 0o777,
                'sha256': hashlib.sha256(native).hexdigest(),
                'compiler_sha256': hashlib.sha256(data).hexdigest()})
        summary = {'country': country, 'profile': profile, 'iso639_3': iso,
                   'native_language': native_label, 'script': script,
                   'source_files': len(manifest['files']),
                   'changed_identifiers': sum(a != b for a, b in names.items()),
                   'proposed_identifiers': sum(row[3] == 'project-proposal' for row in details),
                   'pending_identifiers': sum(row[3] != 'compatibility' and row[3] != 'project-proposal' for row in details),
                   'linguistic_review': 'incomplete', 'source': str(destination.relative_to(root))}
        manifest['summary'] = summary
        (output / '문자대응.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (output / '식별자대응.tsv').write_text(table(['original', 'compiler', 'native', 'status'], details), encoding='utf-8')
        (output / '파일대응표.tsv').write_text(table(['original', 'native'], [[original, paths[current]] for original, current in canonical_paths.items()]), encoding='utf-8')
        shutil.copy2(str(root / 'tools/native_source.py'), str(output / '문자빌드.py'))
        manifest['adapter_sha256'] = hashlib.sha256((output / '문자빌드.py').read_bytes()).hexdigest()
        (output / '문자대응.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (output / 'Makefile').write_text('.PHONY: kernel iso userland verify stage\n.DEFAULT_GOAL := kernel\nkernel iso userland verify stage:\n\tpython3 문자빌드.py $@\n', encoding='utf-8')
        (output / '문자판안내.md').write_text('# ' + country + ' / ' + profile + '\n\n'
            + '이 소스는 WorldOS 원문 식별자 방언입니다. 결합문자를 삭제하지 않습니다. '
            + '`make kernel`, `make iso`, `make userland`는 임시 빌드 공간에서만 표준 Go 이름으로 대응합니다.\n\n'
            + '식별자대응.tsv의 project-proposal은 신규 제안, pending-translation은 미번역, '
            + 'reading-needs-review는 일본어 자동 읽기 검토 대상입니다. 완역·원어민 검수를 뜻하지 않습니다. '
            + '영문 접두부 T/V와 숫자 꼬리는 형식·공개 여부 및 충돌 구분용입니다. '
            + 'C 공개 규약·기계 명령·파일 확장자·Makefile·src·build는 호환성을 위해 보존합니다.\n\n'
            + '기존 파일의 편집 내용은 매 빌드에 반영됩니다. 파일 추가·이동 또는 새 식별자 도입 시 '
            + '문자대응.json의 파일/식별자 대응도 갱신해야 합니다. 미등록 결합문자는 컴파일 오류로 검출됩니다.\n', encoding='utf-8')
        from management_layout import localize_stage
        localize_stage(output, profile)
        # Destination is new; refuse to replace an edition or user modification.
        if destination.exists():
            raise RuntimeError('Destination appeared during generation: ' + str(destination))
        shutil.move(str(output), str(destination))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--resources', type=Path, default=Path('/tmp/worldos-variants-resources'))
    parser.add_argument('--profile', action='append', default=[])
    args = parser.parse_args()
    unknown = set(args.profile) - {record[1] for record in profiles()}
    if unknown:
        parser.error('unknown profile: ' + ', '.join(sorted(unknown)))
    results = []
    for record in profiles():
        if args.profile and record[1] not in args.profile:
            continue
        summary = generate(args.root, record, args.resources)
        results.append(summary)
        print('READY', record[0], record[1], summary['source_files'], 'files', flush=True)
    if not args.profile:
        keys = ['country', 'profile', 'iso639_3', 'native_language', 'script', 'source_files', 'changed_identifiers', 'proposed_identifiers', 'pending_identifiers', 'linguistic_review', 'source']
        (args.root / '문자판-목록.tsv').write_text(table(keys, [[result[k] for k in keys] for result in results]), encoding='utf-8')


if __name__ == '__main__':
    main()
