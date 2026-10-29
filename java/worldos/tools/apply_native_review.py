#!/usr/bin/env python3
"""Rename existing native sources, preserving their implementation and headers."""
import argparse
from bisect import bisect_left
import hashlib
import difflib
from functools import lru_cache
import io
import json
from pathlib import Path
import re
import sys
import tarfile
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'native'))
from terms import names
from generate import identifiers
from naming_review import review
from source_names import rename_source, make_renamer, rename_java_local_alias


def part(char):
    return char in '_$' or unicodedata.category(char)[0] in 'LMN' or unicodedata.category(char) in ('Pc','Cf')


def renamer(changes):
    return make_renamer(changes)


def source_rename(name,text,rename):
    return rename_source(name,text,rename)


def encoded(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
def sha(data):return hashlib.sha256(data).hexdigest()


_ALIAS_MARKER = 'WorldosOwnedBundleAliasMarker'
_SOURCE_TOKEN = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\#[^\n]*|(?:[^\W\d]|_)\w*|\S')


@lru_cache(maxsize=1)
def original_sources():
    from generate import sources
    return sources()


@lru_cache(maxsize=8)
def bundle_alias_context(language, native_name, profile_json, old_items, new_items, owned_key='꾸러미'):
    """Recover which old 'pack' tokens originated in the owned Korean name."""
    from generate import adapt
    old, new = dict(old_items), dict(new_items)
    canonical, _ = adapt(original_sources(), language, native_name, json.loads(profile_json))
    old_names, new_names = make_renamer(old), make_renamer(new)
    marked = dict(old)
    marked[owned_key] = _ALIAS_MARKER
    marker_names = make_renamer(marked)
    paths, texts = {}, {}
    for original, data in canonical.items():
        previous = old_names(original)
        paths[previous] = new_names(original)
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            continue
        if owned_key not in text:
            continue
        assert _ALIAS_MARKER not in text
        before = rename_source(original, text, old_names)
        after = rename_source(original, text, marker_names)
        if before != after:
            texts[previous] = (before, after)
    return paths, texts


@lru_cache(maxsize=512)
def mark_owned_bundle_alias(text, before, after, allow_already=False):
    if text == after:
        return text
    if text == before:
        return after
    expected = list(_SOURCE_TOKEN.finditer(before))
    desired = list(_SOURCE_TOKEN.finditer(after))
    actual = list(_SOURCE_TOKEN.finditer(text))
    if len(expected) != len(desired):
        raise ValueError('Owned bundle alias changes the source token structure')
    changes = {i: b.group() for i, (a,b) in enumerate(zip(expected,desired)) if a.group()!=b.group()}
    indices = sorted(changes)
    matched = {}
    matcher = difflib.SequenceMatcher(None, [m.group() for m in expected], [m.group() for m in actual])
    for block in matcher.get_matching_blocks():
        for index in indices[bisect_left(indices,block.a):bisect_left(indices,block.a+block.size)]:
            matched[index] = actual[block.b+index-block.a]
    missing = set(changes) - set(matched)
    if missing and allow_already:
        desired_matcher = difflib.SequenceMatcher(None, [m.group() for m in desired], [m.group() for m in actual])
        for block in desired_matcher.get_matching_blocks():
            missing.difference_update(range(block.a, block.a+block.size))
    if missing:
        raise ValueError('Cannot safely align an edited bundle alias with its original source')
    for index, token in sorted(matched.items(), key=lambda pair: pair[1].start(), reverse=True):
        text = text[:token.start()] + changes[index] + text[token.end():]
    return text


@lru_cache(maxsize=8)
def standard_integer_context(language, native_name, profile_json, items):
    """Recover standard Integer identities corrupted by an older global rename."""
    from generate import adapt
    mapping = dict(items)
    canonical, _ = adapt(original_sources(), language, native_name, json.loads(profile_json))
    local = make_renamer(mapping)
    corrupt = make_renamer({'Integer': mapping['정수'], 'Stream': mapping['흐름여부']})
    repairs = {}
    for original, data in canonical.items():
        if not original.endswith(('.java', '.py')) or (b'Integer' not in data and b'Stream' not in data):
            continue
        desired = rename_source(original, data.decode('utf-8'), local)
        before = corrupt(desired)
        if before != desired:
            repairs[local(original)] = (before, desired)
    return repairs


@lru_cache(maxsize=8)
def canonical_source_order(language, native_name, profile_json):
    from generate import adapt
    canonical, _ = adapt(original_sources(), language, native_name, json.loads(profile_json))
    return tuple(canonical)


@lru_cache(maxsize=8)
def legacy_reference_context(language, items):
    path = ROOT / 'native/inputs/legacy-role-names' / (language + '.json')
    if not path.is_file():
        return {}, {}
    current = dict(items)
    flags = set()
    for data in original_sources().values():
        flags.update(re.findall(r'''["'](--?[A-Za-z][A-Za-z0-9_-]*)["']''', data.decode('utf-8', 'replace')))
    aliases, options = {k:{v} for k,v in current.items()}, {}
    for variant in json.loads(path.read_text())['variants']:
        changes = {v:current[k] for k,v in variant['names'].items() if k in current and v != current[k]}
        convert = make_renamer(changes)
        for old,new in changes.items():
            aliases.setdefault(old, set()).add(new)
        for flag in flags:
            bad = convert(flag)
            if bad != flag:
                options.setdefault(bad, set()).add(flag)
    return ({k:next(iter(v)) for k,v in aliases.items() if len(v)==1},
            {k:next(iter(v)) for k,v in options.items() if len(v)==1 and k not in flags})


@lru_cache(maxsize=2048)
def repair_legacy_references(text, language, items, suffix):
    aliases, options = legacy_reference_context(language, items)
    if not aliases and not options:
        return text
    if options:
        change = make_renamer(options)
        if suffix in ('.java','.py','.c','.cpp','.h','.json'):
            quoted = re.compile(r'''"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*' ''', re.X)
            text = quoted.sub(lambda m: change(m.group()), text)
        else:
            text = change(text)
    # Older protection of JVM class names also matched a suffix of my-java/
    # and new-java/. Repair only those build paths, without touching APIs.
    paths = re.compile(r'''(?:build/(?:my-java|verification/new-java)/)[^\s'"`<>;,()]+''')
    rename = make_renamer(aliases)
    return paths.sub(lambda m: rename(m.group()), text)


@lru_cache(maxsize=1024)
def reconcile_alias_tokens(text, before, after):
    """Repair aligned legacy substitutions; preserve unaligned custom edits."""
    if text == after or before == after:
        return text, 0
    if text == before:
        return after, 0
    expected = list(_SOURCE_TOKEN.finditer(before))
    desired = list(_SOURCE_TOKEN.finditer(after))
    actual = list(_SOURCE_TOKEN.finditer(text))
    if len(expected) != len(desired):
        raise ValueError('Legacy substitution changes token structure')
    changes = {i:b.group() for i,(a,b) in enumerate(zip(expected,desired)) if a.group()!=b.group()}
    indices = sorted(changes)
    matched = {}
    matcher = difflib.SequenceMatcher(None, [m.group() for m in expected], [m.group() for m in actual])
    for block in matcher.get_matching_blocks():
        for index in indices[bisect_left(indices,block.a):bisect_left(indices,block.a+block.size)]:
            matched[index] = actual[block.b+index-block.a]
    missing = set(changes)-set(matched)
    if missing:
        matcher = difflib.SequenceMatcher(None, [m.group() for m in desired], [m.group() for m in actual])
        for block in matcher.get_matching_blocks():
            missing.difference_update(range(block.a,block.a+block.size))
    for index,token in sorted(matched.items(), key=lambda pair: pair[1].start(), reverse=True):
        text = text[:token.start()] + changes[index] + text[token.end():]
    return text, len(missing)


def plan(folder,config,new,entry,revision):
    old=config['identifiers'];changes={old.get(k,k):new.get(k,k) for k in old.keys()|new.keys() if old.get(k,k)!=new.get(k,k)}
    if not changes:return None
    namespace_only = all(old.get(k,k) == new.get(k,k) for k in (old.keys()|new.keys()) - {'한국','제이코로스'})
    namespace_tokens = re.compile(r'(?<![\w$])L?(?:' + '|'.join(re.escape(k) for k in changes) + r')(?![\w$])') if namespace_only else None
    external={'start','read','write','open','close','size','length','get','set','put','add',
              'remove','append','insert','run','wait','notify','send','recv','connect',
              'accept','bind','listen','seek','tell','find','replace','split','join','pack','Integer','Stream'}
    ambiguous=set(changes)&external
    bundle_paths, bundle_texts = {}, {}
    bundle_change = old.get('꾸러미') == 'pack' and 'pack' in changes
    integer_change = old.get('정수') == 'Integer' and 'Integer' in changes
    alias_key = '꾸러미' if bundle_change else '정수' if integer_change else None
    if alias_key:
        profile=(folder/config['source']/config['native']/'input.json').read_text()
        bundle_paths,bundle_texts=bundle_alias_context(config['language'],config['native_name'],profile,
                                                     tuple(sorted(old.items())),tuple(sorted(new.items())),alias_key)
        ambiguous.discard(old[alias_key])
    scoped = {}
    scoped_aliases = set()
    # This old French/Spanish alias is a boolean local in precisely these two
    # owned Java sources. Standard Set/set calls and JVM method-name strings
    # must retain their external identities everywhere else.
    if old.get('일치여부') == 'set' and 'set' in ambiguous:
        old_paths = make_renamer(old)
        scoped = {config['source']+'/'+old_paths(p): {'set': changes['set']} for p in (
            'platforms/rpi4-native/원문/셸문법.java',
            'platforms/rpi4-native/사용자/자바/자바가상기계.java')}
        ambiguous.remove('set')
        scoped_aliases.add('set')
    if old.get('흐름여부') == 'Stream' and 'Stream' in ambiguous:
        vm = config['source']+'/'+make_renamer(old)('platforms/rpi4-native/사용자/자바/자바가상기계.java')
        scoped.setdefault(vm, {})['Stream'] = changes['Stream']
        scoped_aliases.add('Stream')
        ambiguous.remove('Stream')
    if ambiguous:
        raise ValueError('An old localized alias also names an external API: '+
            ','.join(sorted(ambiguous))+'. Apply the final dictionary to the original owned sources; sequential text renaming would also change standard calls: '+str(folder))
    rename=renamer({k:v for k,v in changes.items() if k not in scoped_aliases and not (alias_key and k==old[alias_key])});manifest=folder/'native-generated.json';previous=json.loads(manifest.read_text())
    profile = (folder/config['source']/config['native']/'input.json').read_text()
    originals = canonical_source_order(config['language'], config['native_name'], profile)
    assert len(originals) == len(config['owned_files']), 'Source inventory length changed'
    old_names, new_names = make_renamer(old), make_renamer(new)
    mismatches = [(a,b) for a,b in zip(originals,config['owned_files']) if old_names(a)!=b]
    assert len(mismatches) < len(originals)//20, 'Cannot safely align source inventory order'
    canonical_paths = {previous:new_names(original) for original,previous in zip(originals,config['owned_files'])}
    stale_paths = {}
    for original, previous_path in mismatches:
        desired_path = new_names(original)
        assert Path(previous_path).suffix == Path(original).suffix, 'Source inventory order mismatch'
        if previous_path != desired_path:
            stale_paths[previous_path] = desired_path
            stale_paths[Path(previous_path).name] = Path(desired_path).name
    path_rename = make_renamer(stale_paths)
    output={};backups={};pending=set();occurrences=0;new_values=set(new.values())
    special={'native.json','native-names.tsv','native-pending.tsv','native-term-evidence.json'}
    for name,expected in previous.items():
        if name in special:continue
        path=folder/name
        if path.is_symlink() or not path.is_file():raise ValueError('Missing or linked owned source: '+str(path))
        data=path.read_bytes();updated=data;localized=rename(name)
        relative=name[len(config['source'])+1:] if name.startswith(config['source']+'/') else None
        if relative in bundle_paths:
            localized=config['source']+'/'+bundle_paths[relative]
        if relative in canonical_paths:
            localized=config['source']+'/'+canonical_paths[relative]
        try:
            text=data.decode('utf-8')
            if relative in bundle_texts:
                text=mark_owned_bundle_alias(text,*bundle_texts[relative])
            if namespace_tokens is None or namespace_tokens.search(text):
                text=source_rename(name,text,rename)
            if stale_paths:
                text=source_rename(name,text,path_rename)
            if alias_key:
                text=text.replace(_ALIAS_MARKER,new[alias_key])
            if name in scoped:
                text=rename_java_local_alias(text,scoped[name])
            updated=text.encode()
            if name.startswith(config['source']+'/') or name.endswith('.java'):
                tokens=identifiers(name,updated.decode());pending.update(t for t in tokens if any('\uac00'<=c<='\ud7a3' for c in t))
                occurrences+=sum(t in new_values for t in tokens)
        except UnicodeDecodeError:pass
        if localized in output:raise ValueError('Rename collision: '+str(folder/localized))
        if localized!=name and (folder/localized).exists() and localized not in previous:raise ValueError('Preserving unowned file: '+str(folder/localized))
        output[localized]=(updated,path.stat().st_mode&0o777)
        if localized!=name or updated!=data:backups[name]=(data,path.stat().st_mode&0o777)
    if config['language'] == 'ko':
        pending.clear()  # Korean is the intended language in a Korean edition.
    config=dict(config,identifiers=new,owned_files=[canonical_paths[n] for n in config['owned_files']],
        examples={k:new.get(k,rename(v)) for k,v in config['examples'].items()})
    for field in ('builder','runner','image_builder','system_tester'):
        if field in config:config[field]=rename(config[field])
    config['naming']=dict(config['naming'],mapped_identifiers=len(new),replaced_occurrences=occurrences,
        untranslated_identifiers=len(pending),functional_review_revision=revision,
        native_review='pending',etymology_review='pending')
    evidence=json.loads((folder/'native-term-evidence.json').read_text())
    evidence['functional_review']={'revision':revision,'references':entry.get('references',[]),
        'verified_lexeme_history':entry.get('verified_lexeme_history',[]),
        'compound_status':'Modern function-based project proposals; native-speaker review pending.'}
    replacements={'native.json':encoded(config),'native-names.tsv':('original\tlocalized\tstatus\n'+''.join(k+'\t'+v+'\tfunctional-proposal\n' for k,v in sorted(new.items()))).encode(),
        'native-pending.tsv':('identifier\tstatus\n'+''.join(k+'\ttranslation-review-required\n' for k in sorted(pending))).encode(),
        'native-term-evidence.json':encoded(evidence)}
    for name,data in replacements.items():
        path=folder/name;prior=path.read_bytes();output[name]=(data,path.stat().st_mode&0o777)
        if data!=prior:backups[name]=(prior,path.stat().st_mode&0o777)
    hashes={name:sha(data) for name,(data,mode) in output.items()}
    backups['native-generated.json']=(manifest.read_bytes(),manifest.stat().st_mode&0o777)
    output['native-generated.json']=(encoded(hashes),0o644)
    # Save only actual changes; retain byte-exact user modifications elsewhere.
    writes={name:value for name,value in output.items() if not (folder/name).is_file() or (folder/name).read_bytes()!=value[0]}
    removed=set(previous)-set(output)
    return {'folder':folder,'writes':writes,'removed':removed,'backups':backups,'language':config['language'],'changes':changes}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    evidence=review();revision=sha(encoded(evidence));plans=[]
    paths=sorted((ROOT/'country').glob('*/native.json'))+sorted((ROOT/'country').glob('*/*/native.json'))
    for number,path in enumerate(paths,1):
        config=json.loads(path.read_text());language=config['language']
        if language not in evidence['languages'] or language=='ko':continue
        from country_naming import names_for_country
        result=plan(path.parent,config,names_for_country(config['country'],language),evidence['languages'][language],revision)
        if result:plans.append(result);print('Planned',path.parent.relative_to(ROOT),len(result['writes']),flush=True)
    report={'applied':args.apply,'editions':len(plans),'languages':sorted({p['language'] for p in plans}),
        'files_changed':sum(len(p['writes']) for p in plans),'paths_removed_after_rename':sum(len(p['removed']) for p in plans),
        'implementation_preserved':True,'copyright_preserved':True,'native_review':'pending','etymology_review':'pending','revision':revision}
    destination=ROOT/'build/naming-review';destination.mkdir(parents=True,exist_ok=True)
    if args.apply and plans:
        archive=destination/'before-native-renaming.tar.gz'
        if archive.exists():raise ValueError('Previous backup exists; preserve it before another application: '+str(archive))
        with tarfile.open(str(archive),'w:gz') as stream:
            for item in plans:
                for name,(data,mode) in item['backups'].items():
                    info=tarfile.TarInfo(str((item['folder']/name).relative_to(ROOT)));info.size=len(data);info.mode=mode
                    stream.addfile(info,io.BytesIO(data))
        for item in plans:
            folder=item['folder']
            for name,(data,mode) in item['writes'].items():
                path=folder/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);path.chmod(mode)
            for name in item['removed']:(folder/name).unlink()
            print('Applied',folder.relative_to(ROOT),flush=True)
    (destination/'native-renaming.json').write_bytes(encoded(report));print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
