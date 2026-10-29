#!/usr/bin/env python3
"""Apply country/language naming to independent source trees, with rollback data."""
import argparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import io
import json
import re
from pathlib import Path
import sys
import tarfile
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'native'))
import apply_native_review as migration
from country_naming import country_policy, validate_edition, names_for_country, country_names, country_source_identity
from terms import names
from source_names import make_renamer, rename_legal_paths, rename_source, escape_python_byte_literals


# Equal source bytes occur in independent editions. Cache computation only;
# every output is written as its own regular file, with its own permissions.
original_renamer = migration.renamer
@lru_cache(maxsize=32)
def cached_renamer(items):
    return original_renamer(dict(items))
migration.renamer = lambda changes: cached_renamer(tuple(sorted(changes.items())))
original_symbol_renamer = make_renamer
@lru_cache(maxsize=32)
def cached_symbol_renamer(items):
    return original_symbol_renamer(dict(items))
migration.make_renamer = lambda changes: cached_symbol_renamer(tuple(sorted(changes.items())))
migration.source_rename = lru_cache(maxsize=4096)(migration.source_rename)
migration.identifiers = lru_cache(maxsize=4096)(migration.identifiers)


def metadata(folder, result, policy, revision, original_config):
    if result is None:
        result = {'folder': folder, 'writes': {}, 'removed': set(), 'backups': {}, 'changes': {}}
    writes, backups = result['writes'], result['backups']
    prior_bytes = {}
    def read(name):
        if name in writes:
            return writes[name][0]
        if name not in prior_bytes:
            prior_bytes[name] = (folder / name).read_bytes()
        return prior_bytes[name]
    def put(name, data):
        path = folder / name
        prior = read(name)
        if data != prior:
            if path.is_file():
                mode = path.stat().st_mode & 0o777
                backups.setdefault(name, (prior, mode))
            else:
                mode = writes[name][1]  # Renamed source; its old path is backed up.
            writes[name] = (data, mode)
    config = json.loads(read('native.json'))
    if config.get('language') == 'ko':
        config['naming']['untranslated_identifiers'] = 0
        put('native-pending.tsv', b'identifier\tstatus\n')
    if (ROOT / 'native/inputs/legacy-role-names' / (config['language']+'.json')).is_file():
        items = tuple(sorted(config['identifiers'].items()))
        for relative in config['owned_files']:
            name = config['source'] + '/' + relative
            data = read(name)
            try:
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                continue
            put(name, migration.repair_legacy_references(text, config['language'], items, Path(relative).suffix).encode('utf-8'))
    if config['language'] == 'zh':
        from terms import HELP
        profile = json.loads((ROOT / 'native/inputs/zh-default-input.json').read_text())
        config['input'] = {k:v for k,v in profile.items() if k not in ('map','altgr')}
        config.update(native_name='中文', help=HELP['zh'], help_sentence_translated=True)
        put(config['source']+'/'+config['native']+'/input.json', migration.encoded(profile))
    from localization_runtime import patches, update, repair_input_help
    for relative, edits in patches(config['identifiers']).items():
        name = config['source'] + '/' + relative
        data = read(name)
        put(name, update(data.decode('utf-8'), edits).encode('utf-8'))
    # These literals are API symbol references, rather than character fixtures.
    # Older copies preserved one-character aliases such as '글' and '값'.
    symbols = make_renamer(config['identifiers'])
    managed = symbols('원천') + '/'
    for relative in config['owned_files']:
        if relative.startswith(managed) and relative.endswith('.java'):
            name = config['source'] + '/' + relative
            text = read(name).decode('utf-8')
            put(name, country_source_identity('원천/'+relative[len(managed):], text, config['identifiers']).encode('utf-8'))
    shell_name = config['source'] + '/' + symbols('platforms/rpi4-native/원문/명령해석기.java')
    shell_data = read(shell_name)
    details = None
    if config['language'] == 'zh':
        details = [config['help'], '  [ZH] candidates; [EN] ASCII',
                   '  ni → 你', '  F9: EN ↔ 中文 | Ctrl+Shift+V: UTF-8',
                   '  空格：下一个候选字；F9：确定并返回英文',
                   '  help input | vi: i ... Esc :wq']
        kernel_name = config['source']+'/'+symbols('platforms/rpi4-native/원문/핵심.java')
        text = read(kernel_name).decode('utf-8')
        text = re.sub(r'"WorldOS zh · [^"\\]* · 😀"', '"WorldOS zh · 你好 · 😀"', text)
        put(kernel_name, text.encode('utf-8'))
        for relative in config['owned_files']:
            if relative.startswith('example/') and Path(relative).suffix in ('.java', '.py', '.c'):
                name = config['source']+'/'+relative
                text = read(name).decode('utf-8')
                text = text.replace(': zh ', ': 你好 ').replace('"zh"', '"中文"').replace("'zh'", "'中文'")
                put(name, text.encode('utf-8'))
    put(shell_name, repair_input_help(shell_data.decode('utf-8'), config['identifiers'], config['help'], details).encode())
    originals = ['platforms/rpi4-native/사용자/자바/자바가상기계.java',
                 'platforms/rpi4-native/명명/시언어이름.json',
                 'platforms/rpi4-native/명명/파이썬이름.json']
    originals += [p for p in config['owned_files'] if p.startswith('platforms/rpi4-native/tools/') and p.endswith('.py')]
    for original in originals if config['identifiers'] else ():
        name = config['source'] + '/' + symbols(original)
        data = read(name)
        put(name, rename_source(original, data.decode('utf-8'), symbols).encode('utf-8'))
    for relative in config['owned_files']:
        if relative.endswith('.py'):
            name = config['source'] + '/' + relative
            put(name, escape_python_byte_literals(read(name).decode('utf-8')).encode('utf-8'))
        if Path(relative).suffix in ('.java', '.py', '.c', '.cpp', '.h'):
            name = config['source'] + '/' + relative
            text = read(name).decode('utf-8')
            text = re.sub(r'\bjava\.nio\.[^\s.;]+\.StandardCharsets\b', 'java.nio.charset.StandardCharsets', text)
            text = text.replace('java.util.stream.' + symbols('흐름여부'), 'java.util.stream.Stream')
            text = text.replace('; ' + symbols('문자부호') + '=', '; charset=')
            put(name, text.encode('utf-8'))
    launcher = 'native-java/' + symbols('국가실행기') + '.java'
    text = read(launcher).decode('utf-8')
    text = migration.repair_legacy_references(text, config['language'], tuple(sorted(config['identifiers'].items())), '.java')
    put(launcher, re.sub(r'\bjava\.nio\.[^\s.;]+\.StandardCharsets\b', 'java.nio.charset.StandardCharsets', text).encode('utf-8'))
    from java_prose import localize_java_comments
    for relative in config['owned_files'] + [launcher]:
        if not relative.endswith('.java'):
            continue
        name = relative if relative == launcher else config['source'] + '/' + relative
        text = read(name).decode('utf-8')
        put(name, localize_java_comments(relative, text, config['language'], config['identifiers'],config['native_name']).encode('utf-8'))
    entry = read('native-launch.sh').decode('utf-8')
    entry,count = re.subn(r'''native-java/[^/\s"']+\.java''', lambda _: launcher, entry)
    assert count == 1, 'Cannot safely identify the native Java launcher reference'
    put('native-launch.sh', entry.encode('utf-8'))
    config['country_naming'] = policy
    config['kernel'] = policy['namespace']['os_name'] + ' own Java AOT ARM64 EL1; not Linux'
    config['naming']['country_naming_revision'] = revision
    put('native.json', migration.encoded(config))
    evidence = json.loads(read('native-term-evidence.json'))
    evidence['country_language_policy'] = policy
    prior_review = migration.review()['languages']
    language = config['language']
    reviewed = prior_review.get(language, prior_review.get({'zh_Hans': 'zh'}.get(language, language), {}))
    if reviewed:
        evidence['functional_review'] = {
            'references': reviewed.get('references', []),
            'verified_lexeme_history': reviewed.get('verified_lexeme_history', []),
            'scope': 'Previously reviewed whole roles; does not certify all new names or compounds.',
            'compound_status': 'Modern function-based project proposals; native-speaker review pending.'}
    evidence['naming_scope'] = 'First-party identifiers and paths; language keywords, external APIs, dependency archives, legal clauses, copyright and literal character values retain their specified identities.'
    evidence['unverified_terms'] = 'native-pending.tsv; terms absent from language dictionaries are not certified translations.'
    snapshot = ROOT / 'native/inputs/localized-roles' / (language + '.json')
    if snapshot.is_file():
        proposals = json.loads(snapshot.read_text())
        evidence['terminology_proposals'] = {key: proposals.get(key) for key in (
            'references', 'archive_sha256', 'archive_member', 'scope', 'status',
            'native_review', 'etymology_review', 'manual_glossary_sha256',
            'whole_role_corrections_sha256', 'naming_principles', 'verified_lexeme_history')}
        evidence['terminology_proposals']['whole_roles'] = len(proposals.get('roles', {}))
        evidence['terminology_proposals']['pending_roles'] = len(proposals.get('pending_roles', {}))
    if config['language'] == 'en':
        evidence['english_word_history'] = {
            'kernel': {'history': 'Old English cyrnel, diminutive of corn; modern OS names are project compounds.',
                       'source': 'https://www.merriam-webster.com/dictionary/kernel'},
            'thread': {'history': 'Middle English thred, from Old English thrǣd; the new execution-related compounds are modern project names.',
                       'source': 'https://www.merriam-webster.com/dictionary/thread'},
            'port': {'history': 'Opening/interface sense: Middle English porte via Anglo-French, from Latin porta (passage, gate). Distinct from the harbour sense.',
                     'source': 'https://www.merriam-webster.com/dictionary/port', 'dictionary_sense': 'noun (2)'},
            'territory_language': 'https://www.gov.ai/stats/abstract00.htm' if config['country'] == 'AIA' else 'Unicode CLDR 48'}
    put('native-term-evidence.json', migration.encoded(evidence))
    legal = json.loads((ROOT / 'native/inputs/legal-sources.json').read_text())['files']
    old_names, new_names = make_renamer(original_config['identifiers']), make_renamer(config['identifiers'])
    # Ownership is checked against the on-disk manifest, before the planned
    # rename. The planned manifest already hashes the translated legal paths.
    previous = json.loads((folder / 'native-generated.json').read_text())
    for original, text in legal.items():
        old_relative, new_relative = old_names(original), new_names(original)
        if old_relative not in original_config['owned_files']:
            continue
        old_name = original_config['source'] + '/' + old_relative
        original_bytes = (folder / old_name).read_bytes()
        assert migration.sha(original_bytes) == previous[old_name], 'Preserving user-edited legal text: ' + str(folder / old_name)
        prior_bytes.setdefault(old_name, original_bytes)
        put(config['source'] + '/' + new_relative, rename_legal_paths(text, new_names).encode())
    hashes = json.loads(read('native-generated.json'))
    for name, (data, mode) in writes.items():
        if name != 'native-generated.json':
            hashes[name] = migration.sha(data)
    for name in result['removed']:
        hashes.pop(name, None)
    put('native-generated.json', migration.encoded(hashes))
    return result


def namespace_metadata(folder, result, policy, revision, original_config):
    """Update namespace evidence without rerunning unrelated language repairs."""
    if result is None:
        result = {'folder': folder, 'writes': {}, 'removed': set(), 'backups': {}, 'changes': {}}
    writes, backups = result['writes'], result['backups']
    def read(name):
        return writes[name][0] if name in writes else (folder / name).read_bytes()
    def put(name, data):
        previous = read(name)
        if data != previous:
            path = folder / name
            if path.is_file():
                mode = path.stat().st_mode & 0o777
                backups.setdefault(name, (path.read_bytes(), mode))
            else:
                mode = writes[name][1]
            writes[name] = data, mode
    config = json.loads(read('native.json'))
    if config.get('language') == 'ko':
        config['naming']['untranslated_identifiers'] = 0
        put('native-pending.tsv', b'identifier\tstatus\n')
    symbols = make_renamer(config['identifiers'])
    managed = symbols('원천') + '/'
    for relative in config['owned_files']:
        if relative.startswith(managed) and relative.endswith('.java'):
            name = config['source'] + '/' + relative
            data = read(name).decode('utf-8')
            put(name, country_source_identity('원천/'+relative[len(managed):], data, config['identifiers']).encode('utf-8'))
    config['country_naming'] = policy
    config['kernel'] = policy['namespace']['os_name'] + ' own Java AOT ARM64 EL1; not Linux'
    config['naming']['country_namespace_revision'] = revision
    put('native.json', migration.encoded(config))
    evidence = json.loads(read('native-term-evidence.json'))
    evidence['country_language_policy'] = policy
    put('native-term-evidence.json', migration.encoded(evidence))
    manifest = json.loads(read('native-generated.json'))
    for name, (data, mode) in writes.items():
        if name != 'native-generated.json':
            manifest[name] = migration.sha(data)
    for name in result['removed']:
        manifest.pop(name, None)
    put('native-generated.json', migration.encoded(manifest))
    return result


def prose_metadata(folder, policy, revision, config):
    """Apply whole comments without replaying unrelated historical repairs."""
    from java_prose import localize_java_comments
    writes, backups = {}, {}
    manifest=json.loads((folder/'native-generated.json').read_text())
    def put(name,data):
        path=folder/name
        old=path.read_bytes()
        if data!=old:
            mode=path.stat().st_mode & 0o777
            backups[name]=old,mode
            writes[name]=data,mode
            manifest[name]=migration.sha(data)
    for name in manifest:
        if name.endswith('.java'):
            text=(folder/name).read_text()
            put(name,localize_java_comments(name,text,config['language'],config['identifiers'],config['native_name']).encode())
    evidence=json.loads((folder/'native-term-evidence.json').read_text())
    evidence['java_prose']={'revision':revision,'scope':'Explicit whole-sentence Java translations; other prose remains pending.'}
    put('native-term-evidence.json',migration.encoded(evidence))
    put('native-generated.json',migration.encoded(manifest))
    return {'folder':folder,'writes':writes,'removed':set(),'backups':backups,'changes':{}}


def prepared_editions(editions, revision, jobs, namespace_only=False, prose_only=False):
    """Read independent editions concurrently; commits/backups stay serial."""
    def prepare(item):
        path, config, policy = item
        mapping = names_for_country(config['country'], config['language'])
        if prose_only and mapping == config['identifiers']:
            return path,config,prose_metadata(path.parent,policy,revision,config)
        if namespace_only:
            mapping = dict(config['identifiers'], **{k:mapping[k] for k in ('한국','제이코로스')})
        result = migration.plan(path.parent, config, mapping, {}, revision)
        update = namespace_metadata if namespace_only else metadata
        return path, config, update(path.parent, result, policy, revision, config)
    iterator = iter(editions)
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        pending = deque()
        for unused in range(jobs):
            item = next(iterator, None)
            if item is not None:
                pending.append(executor.submit(prepare, item))
        while pending:
            yield pending.popleft().result()
            item = next(iterator, None)
            if item is not None:
                pending.append(executor.submit(prepare, item))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--namespace-only', action='store_true', help='Change country namespaces while preserving the current language glossary and runtime sources')
    parser.add_argument('--prose-only', action='store_true', help='Apply whole Java comments without unrelated repairs when names are already current; migrate changed dictionaries normally')
    parser.add_argument('--countries', help='Comma-separated ISO alpha-3 territory codes; default all')
    parser.add_argument('--languages', nargs='+', help='Restrict application to these explicit language tags')
    parser.add_argument('--resume', type=Path, help='Continue a completed-edition checkpoint from the same dictionary revision')
    parser.add_argument('--jobs', type=int, default=4, choices=range(1, 9), help='Concurrent edition reads; writes remain sequential')
    args = parser.parse_args()
    selected = set(args.countries.split(',')) if args.countries else set(country_policy())
    unknown = selected - set(country_policy())
    if unknown:
        parser.error('Unknown country code: ' + ','.join(sorted(unknown)))
    destination = ROOT / 'build/country-localization'
    destination.mkdir(parents=True, exist_ok=True)
    revision_inputs = [
        ROOT / 'native/country_naming.py', ROOT / 'native/inputs/english-functional-names.tsv',
        ROOT / 'native/inputs/english-source-names.json', ROOT / 'native/inputs/english-composed-names.json',
        ROOT / 'native/inputs/legal-sources.json', ROOT / 'native/terms.py',
        ROOT / 'native/localization_runtime.py', ROOT / 'tools/apply_native_review.py',
        ROOT / 'native/inputs/zh-default-input.json', ROOT / 'native/inputs/country-names.json',
        ROOT / 'tools/apply_country_naming.py', ROOT / 'native/source_names.py',
        ROOT / 'native/java_prose.py', ROOT / 'native/inputs/localized-java-prose.json']
    revision_inputs += sorted((ROOT / 'native/inputs/localized-roles').glob('*.json'))
    revision = migration.sha(b''.join(str(p.relative_to(ROOT)).encode() + b'\0' + p.read_bytes() for p in revision_inputs))
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    archive = destination / ('before-' + stamp + '.tar.gz')
    report = {'revision': revision, 'applied': args.apply, 'backup': str(archive) if args.apply else None, 'editions': []}
    completed = set()
    if args.resume:
        if not args.apply:
            parser.error('--resume requires --apply')
        previous = json.loads(args.resume.read_text())
        if not previous.get('applied') or previous['revision'] != revision:
            parser.error('Checkpoint belongs to another dictionary revision')
        report['editions'] = list(previous['editions'])
        report['previous_checkpoints'] = previous.get('previous_checkpoints', []) + [str(args.resume)]
        report['previous_backups'] = previous.get('previous_backups', []) + [previous['backup']]
        completed = {r['path'] for r in report['editions']}
    paths = sorted((ROOT / 'country').glob('*/native.json')) + sorted((ROOT / 'country').glob('*/*/native.json'))
    # Check every territory/script relationship before touching any edition.
    editions = []
    for path in paths:
        config = json.loads(path.read_text())
        policy = validate_edition(path.parent, config)
        if str(path.parent.relative_to(ROOT)) not in completed and config['country'] in selected and (not args.languages or config['language'] in args.languages):
            names_for_country(config['country'], config['language'])
            editions.append((path, config, policy))
    editions.sort(key=lambda item: (item[1]['language'], str(item[0])))
    stream = tarfile.open(str(archive), 'w:gz') if args.apply else None
    try:
        for path, config, result in prepared_editions(editions, revision, args.jobs, args.namespace_only, args.prose_only):
            count = len(result['writes'])
            if args.apply:
                # Save the originals before any path in this edition changes.
                for name, (data, mode) in result['backups'].items():
                    info = tarfile.TarInfo(str((path.parent / name).relative_to(ROOT)))
                    info.size, info.mode = len(data), mode
                    stream.addfile(info, io.BytesIO(data))
                stream.fileobj.flush()
                for name, (data, mode) in result['writes'].items():
                    target = path.parent / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                    target.chmod(mode)
                for name in result['removed']:
                    (path.parent / name).unlink()
                old_directories = {parent for name in result['removed']
                                   for parent in (path.parent / name).parents
                                   if parent != path.parent and path.parent in parent.parents}
                for directory in sorted(old_directories, key=lambda p: -len(p.parts)):
                    try:
                        directory.rmdir()
                    except OSError:
                        pass  # Preserve caches, user files, and nonempty directories.
            updated = json.loads(result['writes'].get('native.json', (path.read_bytes(), 0))[0])
            report['editions'].append({'path': str(path.parent.relative_to(ROOT)), 'country': config['country'],
                'language': config['language'], 'files_changed': count, 'paths_renamed': len(result['removed']),
                'identifiers_changed': len(result['changes']),
                'remaining_identifiers': updated['naming']['untranslated_identifiers']})
            print('APPLIED' if args.apply else 'PLANNED', report['editions'][-1], flush=True)
            if len(report['editions']) % 25 == 0:
                (destination / ('application-' + stamp + '.json')).write_bytes(migration.encoded(report))
    finally:
        if stream:
            stream.close()
    report['country_count'] = len({r['country'] for r in report['editions']})
    report['files_changed'] = sum(r['files_changed'] for r in report['editions'])
    (destination / ('application-' + stamp + '.json')).write_bytes(migration.encoded(report))
    print('COUNTRIES', report['country_count'], 'EDITIONS', len(report['editions']), 'FILES', report['files_changed'], flush=True)


if __name__ == '__main__':
    main()
