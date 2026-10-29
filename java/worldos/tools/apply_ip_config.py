#!/usr/bin/env python3
"""Migrate independent editions to ip.conf, preserving localized names and edits."""
import argparse
import difflib
from functools import lru_cache
import hashlib
import io
import json
import re
from pathlib import Path
import sys
import tarfile
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'native'))
from generate import translate, translate_source

SPEC = json.loads((ROOT/'native/inputs/ip-config-update.json').read_text())
NEEDED = set(re.findall(r'[\w$]+', ''.join(f['path']+f['before_source']+f['after_source'] for f in SPEC['files'])+' 국가실행기'))


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def apply_edits(text, edits, label):
    for before, after in edits:
        if after and after in text:
            continue
        if not after and before not in text:
            continue
        if text.count(before) != 1:
            raise ValueError('Cannot safely patch '+label+'\n'+before)
        text = text.replace(before, after, 1)
    return text


@lru_cache(maxsize=8)
def edits_for(items):
    mapping = dict(items)
    result = []
    for file in SPEC['files']:
        path = file['path']
        old = translate_source(path, file['before_source'], mapping).splitlines(True)
        new = translate_source(path, file['after_source'], mapping).splitlines(True)
        edits = []
        for tag, a, b, c, d in difflib.SequenceMatcher(None,old,new,autojunk=False).get_opcodes():
            if tag == 'equal':
                continue
            if a == b:
                anchor = a-1
                while anchor >= 0 and (not ''.join(old[anchor:a]).strip() or ''.join(old).count(''.join(old[anchor:a])) != 1):
                    anchor -= 1
                if anchor < 0:
                    raise ValueError('No unique patch anchor: '+path)
                before = ''.join(old[anchor:a]); after = before+''.join(new[c:d])
            else:
                before, after = ''.join(old[a:b]), ''.join(new[c:d])
            edits.append((before,after))
        result.append((path, edits))
    return result


def plan(path):
    folder = path.parent
    config = json.loads(path.read_text())
    manifest = json.loads((folder/'native-generated.json').read_text())
    writes = {}
    def put(name, data):
        target = folder/name
        if target.is_file():
            current = target.read_bytes()
            if current == data:
                return
            if sha(current) != manifest.get(name):
                raise ValueError('Preserving edited file: '+str(target))
        writes[name] = data
        manifest[name] = sha(data)
    mapping = config['identifiers']
    scoped = {key:value for key,value in mapping.items() if key in NEEDED}
    for original, edits in edits_for(tuple(sorted(scoped.items()))):
        relative = ('native-java/'+translate('국가실행기.java', scoped) if original=='launcher.java'
                    else config['source']+'/'+translate(original, scoped))
        text = (folder/relative).read_text()
        text = apply_edits(text, edits, str(folder/relative))
        put(relative, text.encode())
    for original, source in [('ip.conf', ROOT/'ip.conf'),
            ('platforms/rpi4-native/tools/ip_config.py', ROOT/'tools/ip_config.py')]:
        relative = original
        put(config['source']+'/'+relative, source.read_bytes())
        if relative not in config['owned_files']:
            config['owned_files'].append(relative)
    config['owned_files'].sort()
    config['ip_configuration'] = {'file':'ip.conf','default_ip':'192.168.0.100',
                                  'loaded_at':'build','shared_worldos_file':True}
    put('native.json', encoded(config))
    text=(folder/'NATIVE.md').read_text()
    header='Network / system: `help system` (standard and local command names both accepted).'
    if 'IP configuration: edit project `ip.conf`;' not in text:
        text=text.replace(header,header+'\nIP configuration: edit project `ip.conf`; default `192.168.0.100/24`, gateway `192.168.0.1`. An `ip.conf` beside `native.json` overrides the shared file. Standalone copies use `'+config['source']+'/ip.conf`. Rebuild/restart after changes; regenerate board images too.')
    put('NATIVE.md',text.replace('10.0.2.20','192.168.0.120').replace('10.0.2.2','192.168.0.1').encode())
    if writes:
        # This manifest is metadata, so check it before replacing the edition.
        writes['native-generated.json'] = encoded(manifest)
    return folder, writes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--countries', nargs='+')
    args = parser.parse_args()
    paths = sorted((ROOT/'country').glob('*/native.json'))+sorted((ROOT/'country').glob('*/*/native.json'))
    paths = [p for p in paths if not args.countries or p.parent.relative_to(ROOT/'country').parts[0] in args.countries]
    paths.sort(key=lambda p:json.loads(p.read_text())['language'])
    plans = [plan(p) for p in paths]  # Preflight every edition before writes.
    native_count = len(plans)
    generated = json.loads((ROOT/'naming/generated-files.json').read_text())
    linux_count = 0
    for path in sorted((ROOT/'country').glob('*/*/edition.json')):
        folder = path.parent
        if args.countries and folder.relative_to(ROOT/'country').parts[0] not in args.countries:
            continue
        writes = {}
        for name in ('edition.py','ip_config.py'):
            target=folder/name; data=(ROOT/'tools'/name).read_bytes()
            current=target.read_bytes() if target.is_file() else None
            relative=str(target.relative_to(ROOT))
            if current != data:
                if current is not None and sha(current) != generated.get(relative):
                    raise ValueError('Preserving edited Linux helper: '+str(target))
                writes[name]=data
            generated[relative]=sha(data)
        plans.append((folder,writes));linux_count+=1
    updated = encoded(generated)
    if updated != (ROOT/'naming/generated-files.json').read_bytes():
        plans.append((ROOT,{'naming/generated-files.json':updated}))
    report = {'applied':args.apply, 'editions':native_count, 'linux_editions':linux_count,
              'files_changed':sum(len(w) for f,w in plans), 'default_ip':'192.168.0.100'}
    output = ROOT/'build/ip-config'; output.mkdir(parents=True, exist_ok=True)
    if args.apply:
        backup = output/('before-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.tar.gz')
        with tarfile.open(str(backup),'w:gz') as archive:
            for folder, writes in plans:
                for name in writes:
                    target = folder/name
                    if target.is_file():
                        data = target.read_bytes(); info = tarfile.TarInfo(str(target.relative_to(ROOT)))
                        info.size=len(data); info.mode=target.stat().st_mode & 0o777
                        archive.addfile(info,io.BytesIO(data))
                archive.fileobj.flush()
                for name, data in writes.items():
                    target=folder/name; target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
        report['backup']=str(backup.relative_to(ROOT))
    (output/'application.json').write_bytes(encoded(report))
    print(json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
