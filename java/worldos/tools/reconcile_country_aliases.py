#!/usr/bin/env python3
"""Repair old alias collisions against the original role context, with backups.

Original English interfaces remain identifiable instead of accidentally being
renamed as an unrelated Korean role. Unaligned custom edits are preserved.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import lru_cache
import io
import json
from pathlib import Path
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'native'))
import apply_native_review as migration
from generate import adapt
from source_names import make_renamer, rename_source
from localization_runtime import repair_input_help


@lru_cache(maxsize=8)
def contexts(language, native_name, profile_text, items):
    mapping = dict(items)
    base, help_text = adapt(migration.original_sources(), language, native_name, json.loads(profile_text))
    variants = json.loads((ROOT/'native/inputs/legacy-role-names'/(language+'.json')).read_text())['variants']
    transforms = [make_renamer({v:mapping[k] for k,v in variant['names'].items() if k in mapping and v!=mapping[k]}) for variant in variants]
    rename = make_renamer(mapping)
    result = {}
    inputs = [(str(Path('source')/name), name, data) for name,data in base.items()]
    inputs.append(('launcher','native/국가실행기.java',(ROOT/'native/국가실행기.java').read_bytes()))
    from commands import profile as command_profile
    inputs.append(('commands','native-commands.json',migration.encoded(command_profile(language))))
    for identity,original,data in inputs:
        try:
            raw = data.decode('utf-8')
            desired = raw if identity=='commands' else rename_source(original, raw, rename)
        except UnicodeDecodeError:
            continue
        if original == 'platforms/rpi4-native/원문/명령해석기.java':
            desired = repair_input_help(desired, mapping, help_text)
        # Mark legacy English-origin collisions before translating Korean
        # roles. Applying the old aliases to already translated text would
        # confuse distinct new roles that happen to share an older spelling.
        repairs = [(transform(raw) if identity=='commands' else rename_source(original, transform(raw), rename), desired) for transform in transforms]
        repairs = [(before,after) for before,after in repairs if before!=after]
        if repairs:
            target = ('native-java/'+mapping['국가실행기']+'.java' if identity=='launcher' else
                      'native-commands.json' if identity=='commands' else 'source/'+rename(original))
            result[target] = repairs
    return result


def prepare(path):
    folder = path.parent
    config = json.loads(path.read_text())
    profile = (folder/config['source']/config['native']/'input.json').read_text()
    repairs = contexts(config['language'],config['native_name'],profile,tuple(sorted(config['identifiers'].items())))
    manifest = json.loads((folder/'native-generated.json').read_text())
    writes,backups,pending = {},{},[]
    for name,edits in repairs.items():
        actual = config['source']+name[len('source'):] if name.startswith('source/') else name
        file = folder/actual
        data = file.read_bytes()
        assert migration.sha(data)==manifest[actual], 'Preserving edited source: '+str(file)
        text = data.decode('utf-8')
        for before,after in edits:
            text,unmatched = migration.reconcile_alias_tokens(text,before,after)
            if unmatched:
                pending.append({'path':actual,'unaligned_tokens_preserved':unmatched})
        text = migration.repair_legacy_references(text, config['language'], tuple(sorted(config['identifiers'].items())), file.suffix)
        updated = text.encode('utf-8')
        if updated!=data:
            mode=file.stat().st_mode&0o777
            backups[actual]=(data,mode);writes[actual]=(updated,mode)
            manifest[actual]=migration.sha(updated)
    config['naming']['legacy_alias_compatibility_review_pending']=pending
    for name,data in [('native.json',migration.encoded(config))]:
        file=folder/name;prior=file.read_bytes()
        if prior!=data:
            mode=file.stat().st_mode&0o777;backups[name]=(prior,mode);writes[name]=(data,mode)
            manifest[name]=migration.sha(data)
    if writes:
        name='native-generated.json';file=folder/name;mode=file.stat().st_mode&0o777
        backups[name]=(file.read_bytes(),mode);writes[name]=(migration.encoded(manifest),mode)
    return folder,writes,backups,pending


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--countries',nargs='+')
    parser.add_argument('--languages',nargs='+',default=['de','fr','es'])
    args=parser.parse_args()
    paths=sorted((ROOT/'country').glob('*/native.json'))+sorted((ROOT/'country').glob('*/*/native.json'))
    paths=[p for p in paths if json.loads(p.read_text())['language'] in args.languages and (not args.countries or p.relative_to(ROOT/'country').parts[0] in args.countries)]
    paths.sort(key=lambda p:(json.loads(p.read_text())['language'],str(p)))
    output=ROOT/'build/localization-round2';output.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    archive=output/('before-alias-reconciliation-'+stamp+'.tar.gz')
    results=[]
    stream=tarfile.open(str(archive),'w:gz') if args.apply else None
    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            for folder,writes,backups,pending in executor.map(prepare,paths):
                if args.apply:
                    for name,(data,mode) in backups.items():
                        member=tarfile.TarInfo(str((folder/name).relative_to(ROOT)));member.size=len(data);member.mode=mode
                        stream.addfile(member,io.BytesIO(data))
                    stream.fileobj.flush()
                    for name,(data,mode) in writes.items():
                        file=folder/name;file.write_bytes(data);file.chmod(mode)
                row={'edition':str(folder.relative_to(ROOT)),'files_changed':len(writes),'unaligned_custom_contexts_preserved':len(pending)}
                results.append(row);print(row,flush=True)
    finally:
        if stream:stream.close()
    report={'applied':args.apply,'backup':str(archive) if args.apply else None,'editions':results}
    (output/('alias-reconciliation-'+stamp+'.json')).write_bytes(migration.encoded(report))


if __name__=='__main__':main()
