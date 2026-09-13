#!/usr/bin/env python3
"""Add a localized guest interpreter to all independent WorldOS editions.

Only new sibling packages and a bounded Makefile target are added. Existing
kernel sources, C ABI wrappers and their naming audits remain unchanged.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import unicodedata

from generate_script_variants import profiles, rows, table, japanese_converter, CYRILLIC
from native_source import safe, inverse
from shell_build import c_transform, shell_transform, verify
from shell_terms import vocabulary, COMMANDS, EXTRA_COMMANDS

PRIVATE = set(('INPUT_LINE_CAPACITY MAX_ARGUMENT_COUNT MAX_SCRIPT_DEPTH script_depth text_length text_equal '
 'write_text write_integer write_error read_line split_arguments print_help command_matches run_input '
 'command_source command_echo command_pwd command_cat command_stat command_pid command_uname command_run '
 'command_udp text length left right position value digit_text size number operation input_descriptor '
 'input_line capacity overflow character bytes_read argument_count arguments current output quote path '
 'buffer file_descriptor file_name status name child_pid wait_status receive_address source_address '
 'source_address_length received_data message_length message receive_socket send_socket received_length '
 'cleanup command_names command_aliases bytes_written command input_stream input').split())
HOST_PRIVATE = 'source_file object_file executable_file include_directory startup_object library_file linker_file build_shell'.split()

# Whole technical compounds need explicit readings: 器 is not うつわ here,
# 引数列 is ひきすうれつ, and 文書 ends in しょ, not かき.
JAPANESE_READINGS = {
    'shell_name': 'めいれいかいしゃくき',
    'build_shell': 'めいれいかいしゃくきをくみたてる',
    'source_file': 'げんぶんしょ', 'executable_file': 'じっこうぶんしょ',
    'arguments': 'ひきすうれつ', 'MAX_ARGUMENT_COUNT': 'さいだいひきすうすう',
    'MAX_SCRIPT_DEPTH': 'めいれいぶんしょのさいだいいれこすう',
    'bytes_read': 'よんだはちけたぐみのかず',
    'bytes_written': 'かきだしたはちけたぐみすう',
    'message_length': 'でんぶんのはちけたぐみすう',
    'received_length': 'じゅしんはちけたぐみすう',
    'text_length': 'もじれつのはちけたぐみすう',
}


def identifier(value):
    value = unicodedata.normalize('NFC', value)
    value = value.replace(' ', '_').replace('-', '_').replace("'", '_').replace('’', '_')
    if not value or any(not (ch == '_' or ch in '\u200c\u200d' or unicodedata.category(ch)[0] in 'LM' or unicodedata.category(ch) == 'Nd') for ch in value):
        raise ValueError('Invalid native identifier: ' + value)
    if len(value.encode('utf-8')) > 235:
        raise ValueError('Native filename/identifier too long: ' + value)
    return value


def editions(root):
    result = [(row[0], root / '나라' / row[0], row[3]) for row in rows(root / '나라-소스-언어선택.tsv')[1:]]
    result += [(country + '/' + profile, root / '문자판' / country / profile, profile) for country, profile, *_ in profiles()]
    return result


def proposal(language, resources):
    base = language
    convert = lambda value: value
    if language.startswith('ja_'):
        base = 'ja'
        if language in ('ja_Hira', 'ja_Kana'):
            convert = japanese_converter(resources, language.split('_')[1])
    elif language.startswith(('sr_', 'bs_')):
        base = language  # No invented automatic semantic translation.
    elif language not in ('zh_Hans', 'zh_Hant', 'ms_Latn'):
        base = language.split('_')[0]
    values = {key: convert(value) for key, value in vocabulary(base).items()}
    if language in ('ja_Hira', 'ja_Kana'):
        for key, reading in JAPANESE_READINGS.items():
            values[key] = ''.join(chr(ord(ch) + 0x60) if '\u3041' <= ch <= '\u3096' else ch for ch in reading) if language == 'ja_Kana' else reading
    # English in an undefined-language country is not a native translation.
    if language == 'und':
        values = vocabulary('en')
    aliases = {command: identifier(values[key]) if key in values else command for command, key in COMMANDS.items()}
    extra = EXTRA_COMMANDS.get(base, ('cd', 'exit'))
    aliases.update(zip(('cd', 'exit'), [identifier(convert(value)) for value in extra]))
    if len(set(aliases.values())) != len(aliases):
        raise ValueError('Ambiguous command aliases for ' + language)
    return values, aliases


def assign(keys, vocabulary):
    result = {}
    used = set(keys)  # Reserve all machine/source names, avoiding inverse capture.
    for key in sorted(keys):
        value = identifier(vocabulary[key]) if key in vocabulary else key
        if value != key:
            original = value
            number = 2
            while value in used:
                value = original + '_' + str(number)
                number += 1
        result[key] = value
        used.add(value)
    inverse(result)
    return result


def make_addition(directory_name):
    return '\n# WorldOS independent command interpreter\n.PHONY: shell shell-verify\nshell:\n\t$(MAKE) -C "' + directory_name + '" all\nshell-verify:\n\t$(MAKE) -C "' + directory_name + '" verify\n'


def install(root, record, resources, refresh=False, rename=False):
    edition, parent, language = record
    entry_file = parent / 'shell-entry.json'
    previous = None
    if entry_file.exists():
        entry = json.loads(entry_file.read_text(encoding='utf-8'))
        directory = safe(parent, entry['directory'])
        config = json.loads((directory / 'shell.json').read_text(encoding='utf-8'))
        verify(directory, config)
        if not refresh:
            return config['summary']
        previous = (directory, config)
    values, aliases = proposal(language, resources)
    directory_name = identifier(values.get('shell_name', 'command interpreter'))
    directory = safe(parent, directory_name)
    if directory.exists() and previous is None:
        raise RuntimeError('Refusing to replace existing directory: ' + str(directory))
    moving = previous is not None and previous[0] != directory
    if moving and (not rename or directory.exists()):
        raise RuntimeError('Shell directory rename requires --refresh --rename and a NEW destination')
    makefile = parent / 'Makefile'
    original_make = makefile.read_text(encoding='utf-8') if makefile.exists() else ''
    if moving and original_make.count(make_addition(previous[0].name)) != 1:
        raise RuntimeError('Cannot rename a customized shell Makefile target')
    if previous is None and ('\nshell:' in original_make or '\nshell-verify:' in original_make):
        raise RuntimeError('Existing shell Makefile target requires manual review: ' + str(makefile))
    names, host_names = assign(PRIVATE, values), assign(HOST_PRIVATE, values)
    includes = {}
    posix_entry = parent / 'posix-entry.json'
    if posix_entry.is_file():
        posix_directory = safe(parent, json.loads(posix_entry.read_text(encoding='utf-8'))['directory'])
        posix_config = json.loads((posix_directory / 'posix.json').read_text(encoding='utf-8'))
        if posix_config['edition'] != edition:
            raise RuntimeError('POSIX interface belongs to another edition')
        vocabulary_with_posix = dict(posix_config['names'])
        vocabulary_with_posix.update(values)
        names = assign(PRIVATE | set(posix_config['names']), vocabulary_with_posix)
        includes = posix_config['includes']
    canonical = (root / 'tools/shell_template.c').read_text(encoding='utf-8')
    native = c_transform(canonical, names, includes)
    if c_transform(native, inverse(names), inverse(includes)) != canonical:
        raise RuntimeError('Non-lossless C transformation: ' + edition)
    host = (root / 'tools/shell_build_template.sh.in').read_text(encoding='utf-8')
    host_native = shell_transform(host, {key: '@{' + value + '}' for key, value in host_names.items()})
    lowered_host = shell_transform(host_native, inverse(host_names))
    if lowered_host != shell_transform(host, {key: key for key in HOST_PRIVATE}):
        raise RuntimeError('Non-lossless host-shell template: ' + edition)
    source_name = directory_name + '.c'
    example_name = directory_name + '.commands'
    host_name = identifier(values.get('build_shell', 'build command interpreter')) + '.sh.in'
    summary = {'edition': edition, 'language': language, 'directory': str(directory.relative_to(root)),
               'private_identifiers': len(PRIVATE), 'native_proposals': sum(key in values for key in PRIVATE),
               'pending_identifiers': sum(key not in values for key in PRIVATE),
               'host_native_proposals': sum(key in values for key in HOST_PRIVATE),
               'native_command_aliases': sum(command != alias for command, alias in aliases.items()),
               'linguistic_review': 'incomplete'}
    if language == 'und':
        summary['native_proposals'] = 0
        summary['host_native_proposals'] = 0
        summary['native_command_aliases'] = 0
        summary['pending_identifiers'] = len(PRIVATE)
    config = {'edition': edition, 'language': language, 'source': source_name, 'host_source': host_name,
              'example_source': example_name,
              'names': names, 'includes': includes, 'host_names': host_names, 'commands': aliases, 'summary': summary,
              'canonical_sha256': hashlib.sha256(canonical.encode()).hexdigest(),
              'host_sha256': hashlib.sha256(lowered_host.encode()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='worldos-shell-') as temporary:
        stage = Path(temporary) / directory_name
        stage.mkdir()
        (stage / source_name).write_text(native, encoding='utf-8')
        (stage / host_name).write_text(host_native, encoding='utf-8')
        header = '/* Native command proposals; ASCII aliases remain accepted. */\n'
        for symbol, items in [('command_names', aliases.keys()), ('command_aliases', aliases.values())]:
            header += 'static const char *' + symbol + '[] = {' + ', '.join(json.dumps(value, ensure_ascii=False) for value in items) + '};\n'
        config['header_sha256'] = hashlib.sha256(header.encode()).hexdigest()
        (stage / 'shell_locale.h').write_text(c_transform(header, names), encoding='utf-8')
        example = '# WorldOS ' + edition + ' UTF-8 command file\n'
        example += aliases['echo'] + ' "WorldOS ' + edition + '"\n'
        example += aliases['help'] + '\n' + aliases['pwd'] + '\n' + aliases['pid'] + '\n'
        (stage / example_name).write_text(example, encoding='utf-8')
        for filename in ('shell_build.py', 'native_source.py'):
            shutil.copy2(str(root / 'tools' / filename), str(stage / filename))
        config['auxiliary_sources'] = []
        for original, target in [('shell_idle.c', 'idle.c'), ('shell_probe.c', 'probe.c')]:
            auxiliary = (root / 'tools' / original).read_text(encoding='utf-8')
            (stage / target).write_text(c_transform(auxiliary, names, includes), encoding='utf-8')
            config['auxiliary_sources'].append({'source': target, 'compiler': target,
                                               'compiler_sha256': hashlib.sha256(auxiliary.encode('utf-8')).hexdigest()})
        (stage / 'Makefile').write_text('.PHONY: all shell verify host-build\nall shell:\n\tpython3 shell_build.py build\nverify:\n\tpython3 shell_build.py verify\nhost-build:\n\tpython3 shell_build.py host-build\n', encoding='utf-8')
        mapping = [[key, names[key], 'project-proposal' if key in values and language != 'und' else 'pending-language-review'] for key in sorted(PRIVATE)]
        (stage / '이름대응.tsv').write_text(table(['compiler_identifier', 'native_identifier', 'status'], mapping), encoding='utf-8')
        (stage / '사용자영역선언대응.tsv').write_text(table(['compiler_identifier', 'native_identifier'],
            [[key, value] for key, value in sorted(names.items()) if key not in PRIVATE and key != value]), encoding='utf-8')
        (stage / '셸이름대응.tsv').write_text(table(['compiler_identifier', 'native_identifier'], sorted(host_names.items())), encoding='utf-8')
        (stage / '명령대응.tsv').write_text(table(['ascii_command', 'native_proposal'], aliases.items()), encoding='utf-8')
        (stage / 'README.md').write_text('# ' + edition + ' command interpreter\n\n'
            '이 폴더는 현지어 원문 식별자 C 소스와 명시적인 `@{현지어식별자}` 빌드 셸 틀을 포함합니다. '
            '`make`가 실행 시점에만 컴파일 대응명으로 바꿉니다. `.sh.in`은 Bash 직접 실행 파일이 아닙니다. '
            '다른 국가나 공용 소스가 아니라, 같은 운영체제의 `../posix-<국가코드>` 함수모음을 사용합니다. '
            '새 POSIX 폴더가 아직 없는 경우에만 같은 판의 `../소스` 안 기존 함수모음을 사용합니다.\n\n'
            '`make` → `build/worldos-shell`; `make verify` → 원문·대응 검사. '
            '커널이 읽는 시험 디스크의 USER1 자리에 실행파일을 설치하면 명령해석기로 시작합니다. '
            '원본 가상 디스크를 덮어쓰지 말고 전용 복제를 사용하세요.\n\n'
            '지원: help echo pwd cd cat stat pid uname run udp source exit 및 명령대응.tsv의 별칭. '
            'UTF-8 명령파일은 `source /파일명`으로 읽습니다. 공백·따옴표·역슬래시·행 끝 주석을 처리합니다. '
            '이 폴더의 `.commands` 예제는 새 시험 디스크의 `/COMMANDS`로 복사되며 `source /commands`로 실행합니다. '
            '최대 입력 511바이트, 인수 15개, 명령파일 중첩 4단계. '
            '변수 확장·파이프·재지정·조건문·반복문·작업 제어가 없는 작은 명령해석기이며 POSIX sh 전체 구현이 아닙니다.\n\n'
            '새 이름은 프로젝트 제안이며 원어민 감수·전체 완역을 뜻하지 않습니다. '
            '미번역은 이름대응.tsv에 남습니다. 영어 진단 문구, C/POSIX ABI와 빌드 도구 인터페이스는 유지합니다. '
            '코드 편집은 다음 빌드에 반영되지만 새 현지어 식별자는 shell.json에도 등록해야 합니다. '
            '현재 화면·자판이 모든 문자의 표시·직접 입력을 지원하는 것은 아니며 UTF-8 파일/직렬 로그로 검사합니다.\n', encoding='utf-8')
        from management_layout import localize_stage
        localize_stage(stage, language)
        config['hashes'] = {str(path.relative_to(stage)): hashlib.sha256(path.read_bytes()).hexdigest() for path in stage.iterdir() if path.is_file()}
        (stage / 'shell.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        verify(stage, config)
        if previous is not None:
            verify(previous[0], previous[1])
            for item in stage.iterdir():
                target = previous[0] / item.name
                if target.exists() and item.name not in previous[1]['hashes'] and item.name != 'shell.json':
                    raise RuntimeError('Refusing to overwrite untracked shell file: ' + str(target))
            if not moving:
                backup = Path(tempfile.mkdtemp(prefix='worldos-shell-refresh-backup-'))
                for relative in list(previous[1]['hashes']) + ['shell.json']:
                    target = safe(backup, relative)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(safe(previous[0], relative)), str(target))
                print('REFRESH BACKUP', edition, backup, flush=True)
            if moving:
                if makefile.read_text(encoding='utf-8') != original_make:
                    raise RuntimeError('Country Makefile changed during migration')
                backup = Path(tempfile.mkdtemp(prefix='worldos-shell-rename-backup-'))
                shutil.copytree(str(previous[0]), str(backup / previous[0].name), symlinks=True)
                shutil.copy2(str(makefile), str(backup / 'Makefile'))
                shutil.copy2(str(entry_file), str(backup / 'shell-entry.json'))
                if directory.exists():
                    raise RuntimeError('Rename destination appeared during migration')
                previous[0].rename(directory)
                print('RENAMED', edition, previous[0].name, '->', directory.name, 'backup:', backup, flush=True)
            for item in stage.iterdir():
                shutil.copy2(str(item), str(directory / item.name))
            if moving:
                for obsolete in set(previous[1]['hashes']) - set(config['hashes']):
                    safe(directory, obsolete).unlink()  # Hash-verified generated files; retained in the complete backup.
                makefile.write_text(original_make.replace(make_addition(previous[0].name), make_addition(directory_name)), encoding='utf-8')
                entry_file.write_text(json.dumps({'directory': directory_name}, ensure_ascii=False) + '\n', encoding='utf-8')
        else:
            if directory.exists():
                raise RuntimeError('Destination appeared during generation')
            shutil.move(str(stage), str(directory))
    if previous is not None:
        return summary
    entry_file.write_text(json.dumps({'directory': directory_name}, ensure_ascii=False) + '\n', encoding='utf-8')
    if makefile.exists() and makefile.read_text(encoding='utf-8') != original_make:
        raise RuntimeError('Country Makefile changed during installation')
    makefile.write_text(original_make + make_addition(directory_name), encoding='utf-8')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', action='append', default=[])
    parser.add_argument('--resources', type=Path, default=Path('/tmp/worldos-variants-resources'))
    parser.add_argument('--refresh', action='store_true', help='update only hash-verified, unedited generated shell files')
    parser.add_argument('--rename', action='store_true', help='allow a generated directory rename with a complete backup')
    args = parser.parse_args()
    if args.rename and not args.refresh:
        parser.error('--rename requires --refresh')
    records = editions(args.root)
    unknown = set(args.edition) - {record[0] for record in records}
    if unknown:
        parser.error('unknown editions: ' + ', '.join(sorted(unknown)))
    reports = []
    for record in records:
        if args.edition and record[0] not in args.edition:
            continue
        summary = install(args.root, record, args.resources, args.refresh, args.rename)
        reports.append(summary)
        print('READY', record[0], summary['native_proposals'], 'private-name proposals', flush=True)
    if not args.edition:
        header = ['edition', 'language', 'directory', 'private_identifiers', 'native_proposals', 'pending_identifiers', 'host_native_proposals', 'native_command_aliases', 'linguistic_review']
        (args.root / '명령해석기-목록.tsv').write_text(table(header, [[row[key] for key in header] for row in reports]), encoding='utf-8')


if __name__ == '__main__':
    main()
