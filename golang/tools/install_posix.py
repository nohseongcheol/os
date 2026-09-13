#!/usr/bin/env python3
"""Install independent native POSIX packages beside existing WorldOS sources."""
import argparse
import json
from pathlib import Path
import re
import shutil
import tempfile

from generate_script_variants import rows, table, profiles
from install_shells import editions, identifier, assign
from native_source import safe, inverse, paths_transform, tokens, local_path
from neutralize_posix import neutral
from posix_build import c_transform, c_identifiers, application_maps, digest, verify
from posix_terms import explicit, FUNCTION_KEYS, LOCAL_KEYS
from posix_library_terms import FUNCTION_KEYS as LIBRARY_FUNCTION_KEYS
from shell_terms import vocabulary
from variant_terms import terms as script_terms
from posix_declaration_terms import KEYS as DECLARATION_KEYS, CATEGORIES, meanings
from management_layout import localize_stage

C_SYNTAX = set(('auto break case char const continue default do double else enum extern float for goto if inline int long '
    'register restrict return short signed sizeof static struct switch typedef union unsigned void volatile while '
    'define elif endif error ifdef ifndef include pragma undef __cplusplus __LINE__ __FILE__ __asm__ __volatile__ '
    '__attribute__ noreturn').split())
ABI_NAMES = {'main', '_start', '__syscall6', '__syscall_result'}


def preserved_reason(word, language=None):
    if word in C_SYNTAX:
        return 'c-or-preprocessor-syntax'
    if word.startswith('__builtin_'):
        return 'compiler-intrinsic'
    if word in ABI_NAMES:
        return 'abi-entry-or-explicit-neutral-name'
    if language == 'en':
        return 'english-source'
    return 'pending-language-review'


def language_code(language):
    base = language.split('_')[0]
    codes = json.loads(Path('/usr/share/iso-codes/json/iso_639-3.json').read_text())['639-3']
    aliases = {row.get('alpha_2', row['alpha_3']): row['alpha_3'] for row in codes}
    aliases.update({'zh': 'zho', 'und': 'und'})
    return aliases.get(base, base)


def terminology(tree, language):
    values, paths = explicit(language)
    status = {key: 'project-proposal' for key in values}
    base = language if language.startswith('zh_') else language.split('_')[0]
    # Only role-equivalent fields, not arbitrary concatenated dictionary words.
    fields = vocabulary(base)
    equivalents = {'fd': 'file_descriptor', 'buf': 'buffer', 'buffer': 'buffer',
        'argv': 'arguments', 'arguments': 'arguments', 'path': 'path', 'value': 'value',
        'length': 'length', 'size': 'size', 'status': 'status', 'name': 'name'}
    if language not in ('ja_Hira', 'ja_Kana'):
        for key, equivalent in equivalents.items():
            if key not in values and equivalent in fields:
                values[key] = fields[equivalent]
                status[key] = 'project-proposal'
    if not local_path(tree, '문자대응.json').is_file():
        glossary = local_path(tree, '용어사전.tsv')
        if glossary.is_file():
            words = {row[0]: row[1] for row in rows(glossary)[1:]}
            for key in ('read', 'write', 'open', 'close'):
                if key not in values and words.get(key, key) != key:
                    values[key] = words[key]
                    status[key] = 'inherited-proposal-needs-review'
    script = script_terms(language)
    for key in ('read', 'write', 'size'):
        if key not in values and key in script:
            values[key] = script[key]
            status[key] = 'project-proposal'
    if base == 'en':
        for key in FUNCTION_KEYS + LOCAL_KEYS:
            values.setdefault(key, key)
            status[key] = 'english-source'
    values = {key: ('_' + value if value[0].isdigit() else value) for key, value in values.items()}
    return values, paths, status


def canonical_sources(tree):
    mapping = dict(rows(local_path(tree, '파일대응표.tsv'))[1:])
    prefix = 'userland/posix/'
    base = safe(tree, mapping[prefix + 'Makefile']).parent
    reverse = {str(safe(tree, native).relative_to(base)): original[len(prefix):].replace('engos/syscall.h', 'sys/syscall.h')
        for original, native in mapping.items() if original.startswith(prefix)}
    for original in ('include/unistd.h', 'src/unistd.c', 'tests/runtime.c'):
        local = str(safe(tree, mapping[prefix + original]).relative_to(base).parent)
        reverse[local] = original.split('/')[0]
    sources = {}
    provenance = {}
    for original, relative in mapping.items():
        if not original.startswith(prefix) or original.endswith('.md'):
            continue
        compiler = original[len(prefix):].replace('engos/syscall.h', 'sys/syscall.h')
        raw = safe(tree, relative).read_bytes()
        text = neutral(raw.decode('utf-8'))
        if compiler == 'Makefile':
            # Variant Makefiles deliberately retain compiler-side -I operands.
            # This freestanding library has exactly one private include root.
            if len(re.findall(r'-I\S+', text)) != 1 or '-nostdinc' not in text:
                raise RuntimeError('Unexpected POSIX include configuration')
            text = re.sub(r'-I\S+', '-Iinclude', text)
            text = paths_transform(text, reverse)
        if compiler.endswith('.h'):
            # The standard header used "socket" as a parameter and function name.
            # Give that parameter its own role before localizing the function.
            text = text.replace('int socket,', 'int fd,')
        sources[compiler] = text.encode('utf-8')
        provenance[compiler] = {'source': relative, 'sha256': digest(raw)}
    return sources, provenance


def addition(directory):
    return '\n# WorldOS independent native POSIX\n.PHONY: posix posix-verify\nposix:\n\t$(MAKE) -C "' + directory + '" all\nposix-verify:\n\t$(MAKE) -C "' + directory + '" verify\n'


def package_directory(edition):
    country = edition.split('/')[0]
    if not re.fullmatch('[A-Z]{3}', country):
        raise ValueError('Expected uppercase three-letter country code: ' + edition)
    return 'posix-' + country


def add_library_sources(root, sources, provenance):
    template = root / 'tools/posix_library'
    for path in sorted(template.rglob('*')):
        if not path.is_file():
            continue
        relative = str(path.relative_to(template))
        if relative in sources:
            raise RuntimeError('Library addition collides with original source: ' + relative)
        sources[relative] = path.read_bytes()
        provenance[relative] = {'template': str(path.relative_to(root)), 'sha256': digest(sources[relative])}
    make = sources['Makefile'].decode('utf-8')
    marker = '\n.PHONY: all clean check runtime test-programs\n'
    if make.count(marker) != 1:
        raise RuntimeError('Unexpected compiler Makefile')
    make = make.replace(marker, '\nOBJECTS += $(BUILD)/string.o $(BUILD)/ctype.o $(BUILD)/stdlib.o $(BUILD)/allocation.o\n' + marker)
    make += '\n# User-space C/POSIX library additions\n$(BUILD)/%.o: src/%.c | $(BUILD)\n\t$(CC) $(CFLAGS) -c $< -o $@\n'
    sources['Makefile'] = make.encode('utf-8')


def install(root, record, refresh=False, rename=False):
    edition, parent, language = record
    directory_name = package_directory(edition)
    tree = local_path(parent, '소스')
    target = parent / directory_name
    previous = None
    if (parent / 'posix-entry.json').exists():
        entry = json.loads((parent / 'posix-entry.json').read_text(encoding='utf-8'))
        existing = safe(parent, entry['directory'])
        config = json.loads((existing / 'posix.json').read_text(encoding='utf-8'))
        verify(existing, config)
        if not refresh:
            return config['summary']
        if existing != target:
            raise RuntimeError('Package directory change requires manual migration')
        previous = config
    if previous is None and (target.exists() or target.is_symlink()):
        raise RuntimeError('Refusing existing destination: ' + str(target))
    makefile = parent / 'Makefile'
    original_make = makefile.read_text(encoding='utf-8')
    if previous is None and ('\nposix:' in original_make or '\nposix-verify:' in original_make):
        raise RuntimeError('Existing POSIX targets need manual review')
    sources, provenance = canonical_sources(tree)
    add_library_sources(root, sources, provenance)
    sources['tests/probe.c'] = (root / 'tools/posix_probe.c').read_bytes()
    values, path_values, statuses = terminology(tree, language)
    paths = {}
    for compiler in sources:
        parts = []
        for part in Path(compiler).parts:
            component = Path(part)
            stem = component.stem if component.suffix else part
            parts.append(identifier(path_values.get(stem, stem)) + component.suffix)
        paths[compiler] = '/'.join(parts)
    inverse(paths)
    includes = {compiler[len('include/'):]: native.split('/', 1)[1] for compiler, native in paths.items() if compiler.startswith('include/')}
    inverse(includes)
    words = set()
    for compiler, data in sources.items():
        if compiler.endswith(('.c', '.h')):
            words.update(c_identifiers(data.decode('utf-8')))
    # Reserve every existing C token, preventing a new name from capturing an
    # unrelated unchanged identifier during inverse lowering.
    selected = set(FUNCTION_KEYS + LOCAL_KEYS + DECLARATION_KEYS)
    for compiler, data in sources.items():
        if compiler.endswith('.h') and paths[compiler] != compiler:
            match = re.search(r'(?m)^#ifndef\s+(\w+)', data.decode('utf-8'))
            if match:
                guard = match.group(1)
                values[guard] = '_' + '_'.join(str(Path(paths[compiler]).with_suffix('')).split('/'))
                statuses[guard] = 'derived-from-native-header-path'
                selected.add(guard)
    names = assign(words | selected, values)
    for key in sorted(words):
        for prefix, namespace in (('SYS_', 'syscall'), ('SC_', 'socket')):
            function = key[len(prefix):] if key.startswith(prefix) else ''
            function = '_exit' if function == 'exit' else function
            if function in FUNCTION_KEYS:
                proposed = identifier(path_values.get(namespace, prefix.rstrip('_'))) + '_' + names[function]
                if proposed in names.values() and names.get(key) != proposed:
                    raise ValueError('Ambiguous syscall constant: ' + key)
                names[key] = proposed
                statuses[key] = 'derived-from-call-role'
                selected.add(key)
    inverse(names)
    summary = {'edition': edition, 'language': language, 'directory': str(target.relative_to(root)),
        'functions': len(FUNCTION_KEYS), 'named_functions': sum(key in values for key in FUNCTION_KEYS),
        'variables': len(LOCAL_KEYS), 'named_variables': sum(key in values for key in LOCAL_KEYS),
        'pending_functions': [key for key in FUNCTION_KEYS if key not in values],
        'new_library_functions': len(LIBRARY_FUNCTION_KEYS),
        'declarations': len(DECLARATION_KEYS),
        'named_declarations': sum(key in values for key in DECLARATION_KEYS),
        'pending_declarations': [key for key in DECLARATION_KEYS if key not in values],
        'pending_c_identifiers': sorted(word for word in words if names.get(word, word) == word and preserved_reason(word, language) == 'pending-language-review'),
        'implementation_scope': 'partial-POSIX-single-thread-C-locale-i386',
        'linguistic_review': 'incomplete'}
    config = {'edition': edition, 'language': language, 'names': names, 'includes': includes,
              'files': [], 'provenance': provenance, 'summary': summary}
    if previous:
        for field, aliases_field in (('names', 'name_aliases'), ('includes', 'include_aliases')):
            aliases = dict(previous.get(aliases_field, {}))
            aliases.update({native: standard for standard, native in previous[field].items()
                            if native != standard and config[field].get(standard) != native})
            config[aliases_field] = aliases
        application_maps(config)
    with tempfile.TemporaryDirectory(prefix='worldos-posix-install-') as temporary:
        stage = Path(temporary) / directory_name
        stage.mkdir()
        for compiler, data in sources.items():
            # The package root Makefile is a native-dialect frontend, while the
            # original Makefile is staged as compiler input from an audited path.
            native = paths[compiler] if compiler != 'Makefile' else 'compiler.mk.in'
            kind = 'c' if compiler.endswith(('.c', '.h')) else 'copy'
            translated = c_transform(data.decode('utf-8'), names, includes).encode('utf-8') if kind == 'c' else data
            out = safe(stage, native)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(translated)
            config['files'].append({'compiler': compiler, 'native': native, 'kind': kind, 'compiler_sha256': digest(data)})
        for filename in ('posix_build.py', 'native_source.py'):
            shutil.copy2(str(root / 'tools' / filename), str(stage / filename))
        (stage / 'Makefile').write_text('.PHONY: all verify\nall:\n\tpython3 posix_build.py build\nverify:\n\tpython3 posix_build.py verify\n', encoding='utf-8')
        (stage / '이름대응.tsv').write_text(table(['standard_identifier', 'native_identifier', 'category', 'status'],
            [[key, names[key], 'function' if key in FUNCTION_KEYS else CATEGORIES.get(key, 'variable' if key in LOCAL_KEYS else 'internal-name'), statuses.get(key, 'pending-language-review')]
             for key in sorted(selected)]), encoding='utf-8')
        (stage / '파일대응.tsv').write_text(table(['compiler_file', 'native_file'], [[e['compiler'], e['native']] for e in config['files']]), encoding='utf-8')
        (stage / '기능범위.tsv').write_text(table(['function', 'native_identifier', 'implementation', 'limits'],
            [[key, names[key], 'userspace-library' if key in LIBRARY_FUNCTION_KEYS else 'existing-kernel-wrapper',
              'single-thread;C-locale;byte-strings;i386' if key in LIBRARY_FUNCTION_KEYS else 'kernel-dependent;not-full-POSIX']
             for key in FUNCTION_KEYS]), encoding='utf-8')
        # Record every untouched C name, not just the selected vocabulary's gaps.
        (stage / '보존식별자.tsv').write_text(table(['identifier', 'status'],
            [[word, preserved_reason(word, language)] for word in sorted(words) if names.get(word, word) == word]), encoding='utf-8')
        descriptions = meanings()
        (stage / '선언용어근거.tsv').write_text(table(['standard_identifier', 'native_identifier', 'category', 'current_role', 'status'],
            [[key, names[key], CATEGORIES[key], descriptions[key], statuses.get(key, 'pending-language-review')]
             for key in DECLARATION_KEYS]), encoding='utf-8')
        (stage / 'README.md').write_text('# ' + edition + ' / ' + directory_name + '\n\n'
            '현지어 C 원문과 선언을 포함하는 독립 POSIX 함수모음입니다. 다른 판의 소스를 빌드 중 읽지 않습니다.\n\n'
            '`make`로 `build/libposix.a`, 시작 코드와 시험 실행파일을 만듭니다. '
            '`make verify`는 대응·감사 해시를 검사합니다. '
            '`python3 posix_build.py compile --source 사용자.c --output 새실행파일`은 현지어 응용 코드를 변환·연결합니다.\n\n'
            '이름대응.tsv의 함수·변수를 원문에서 사용합니다. 파일대응.tsv에 현지어 선언 파일 경로가 있습니다. '
            '번역 원문은 모든 문자의 결합부호를 받는 C 방언이며, 빌드 시에만 표준 POSIX 연결 이름으로 낮춥니다. '
            '일반 GCC에 직접 전달하는 표준 C 파일이나 별도의 기계어 ABI가 아닙니다. '
            '표준 헤더와 기계어 연결 이름은 build 아래에 생성됩니다.\n\n'
            '범위: 현재 구현의 ' + str(len(FUNCTION_KEYS)) + '개 공개 함수와 ' + str(len(LOCAL_KEYS)) + '개 선택 구현/매개변수/자료형 이름. '
            '주소형·구조체 필드·상수·오류 코드·보조 이름도 선언용어근거.tsv의 현재 역할에 따라 번역합니다. '
            '언어별 제안이 없는 항목과 C 문법·시작 진입점은 보존식별자.tsv에 사유를 구분해 남깁니다. '
            '미번역 항목은 pending-language-review, 기존 사전에서 가져온 기본 동사는 inherited-proposal-needs-review입니다. '
            '모든 언어 완역이나 원어민 감수를 주장하지 않습니다.\n\n'
            '`__syscall6` / `__syscall_result` / `sys/syscall.h` / `libposix.a`는 OS 중립 이름입니다. '
            '그러나 구현은 i386 int 0x80 및 이 커널의 호출 규약에 의존하므로 이름 변경이 타 커널 이식 완료를 뜻하지 않습니다. '
            'uname은 실행 중인 커널의 실제 정보이며 명칭을 현지어 함수모음이 조작하지 않습니다. '
            'POSIX 표준 전체 구현이나 인증을 뜻하지 않습니다. 일부 선언의 실제 지원 범위는 커널에 따릅니다.\n', encoding='utf-8')
        with (stage / 'README.md').open('a', encoding='utf-8') as stream:
            stream.write('\n추가 함수: 문자열·기억 내용·C 로케일 문자 분류·정수 변환·정렬/검색·환경값 읽기·동적 기억공간 관리. '
                '`build/posix-library-runtime`과 현지어 호출 시험에서 동작을 검사합니다. '
                '문자열 길이는 UTF-8 문자 수가 아니라 바이트 수이며, 문화권별 정렬·유니코드 문자 분류는 미구현입니다. '
                'malloc 계열과 errno는 단일 스레드 한정입니다. realloc(p, 0)은 해제 가능한 최소 영역을 유지합니다. '
                'stdio, 신호, 스레드, 시간, 파일시스템 변경 등 POSIX 전체 기능은 아직 완료되지 않았습니다.\n')
        localize_stage(stage, language)
        config['hashes'] = {str(p.relative_to(stage)): digest(p.read_bytes()) for p in stage.rglob('*') if p.is_file()}
        (stage / 'posix.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        verify(stage, config)
        if makefile.read_text(encoding='utf-8') != original_make:
            raise RuntimeError('Parent Makefile changed during installation')
        if previous:
            verify(target, previous)
            for relative in config['hashes']:
                if safe(target, relative).exists() and relative not in previous['hashes']:
                    raise RuntimeError('Refusing to replace untracked file: ' + relative)
            obsolete = set(previous['hashes']) - set(config['hashes'])
            if obsolete and not rename:
                raise RuntimeError('File rename requires explicit migration: ' + str(obsolete))
            backup = Path(tempfile.mkdtemp(prefix='worldos-posix-refresh-backup-'))
            for relative in list(previous['hashes']) + ['posix.json']:
                dest = safe(backup, relative)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(safe(target, relative)), str(dest))
            installed = []
            try:
                for source in stage.rglob('*'):
                    if source.is_file():
                        relative = str(source.relative_to(stage))
                        dest = safe(target, relative)
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        installed.append(relative)
                        shutil.copy2(str(source), str(dest))
                # Retire only hash-verified generated paths, retaining their
                # original content in the backup. Untracked user files stay put.
                for relative in sorted(obsolete):
                    retired = safe(backup, 'retired/' + relative)
                    retired.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(safe(target, relative)), str(retired))
                verify(target, config)
            except Exception:
                for relative in installed:
                    if relative not in previous['hashes'] and relative != 'posix.json' and safe(target, relative).is_file():
                        failed = safe(backup, 'failed/' + relative)
                        failed.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(safe(target, relative)), str(failed))
                for relative in list(previous['hashes']) + ['posix.json']:
                    dest = safe(target, relative)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(safe(backup, relative)), str(dest))
                raise
            directories = {parent_path for relative in obsolete for parent_path in Path(relative).parents if str(parent_path) != '.'}
            for relative in sorted(directories, key=lambda path: len(path.parts), reverse=True):
                try:
                    safe(target, relative).rmdir()  # Only empty former generated directories.
                except OSError:
                    pass
            print('REFRESH BACKUP', edition, backup, flush=True)
        elif target.exists():
            raise RuntimeError('Destination appeared during installation')
        else:
            shutil.move(str(stage), str(target))
    if previous:
        return summary
    (parent / 'posix-entry.json').write_text(json.dumps({'directory': directory_name}, ensure_ascii=False) + '\n', encoding='utf-8')
    makefile.write_text(original_make + addition(directory_name), encoding='utf-8')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', action='append', default=[])
    parser.add_argument('--refresh', action='store_true', help='refresh only unedited, hash-verified generated files, with a backup')
    parser.add_argument('--rename', action='store_true', help='allow audited source/header path migration, retaining retired files in backup')
    args = parser.parse_args()
    records = editions(args.root)
    if set(args.edition) - {row[0] for row in records}:
        parser.error('Unknown edition')
    summaries = []
    for record in records:
        if not args.edition or record[0] in args.edition:
            summary = install(args.root, record, args.refresh, args.rename)
            summaries.append(summary)
            print('INSTALLED', summary['edition'], summary['named_functions'], '/', summary['functions'], 'function names', flush=True)
    if not args.edition:
        (args.root / 'POSIX-목록.tsv').write_text(table(['edition', 'language', 'directory', 'named_functions', 'functions', 'named_variables', 'variables'],
            [[str(s[key]) for key in ('edition', 'language', 'directory', 'named_functions', 'functions', 'named_variables', 'variables')] for s in summaries]), encoding='utf-8')
        (args.root / 'POSIX-선언-현지화.tsv').write_text(table(['edition', 'language', 'named_declarations', 'declarations', 'pending_c_identifiers'],
            [[str(s[key]) for key in ('edition', 'language', 'named_declarations', 'declarations')] + [str(len(s['pending_c_identifiers']))]
             for s in summaries]), encoding='utf-8')


if __name__ == '__main__':
    main()
