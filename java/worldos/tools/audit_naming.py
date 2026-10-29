#!/usr/bin/env python3
"""Audit language coverage, function roles, filenames and native source ownership."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
from naming_review import COPYRIGHT, matches_owned, review

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/naming-review'
JAVA_KEYWORDS=set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null _'.split())


def sha(data):return hashlib.sha256(data).hexdigest()
def dump(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native',action='store_true',help='Inspect every owned native Java source too')
    parser.add_argument('--record-copyright',action='store_true',help='Record only the already authorized copyright-only changes')
    parser.add_argument('--compile',action='store_true',help='Compile all Linux edition sources together, in their independent packages')
    args=parser.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    terms=json.loads((ROOT/'naming/terms.json').read_text());editions=json.loads((ROOT/'editions.json').read_text());proof=review()
    languages={};failures=[];pending=[]
    for language,rows in terms.items():
        used=set();missing=[];unchecked=[];collisions=[]
        for key,row in rows.items():
            symbol=row['identifier']
            if not symbol.isidentifier() or symbol in JAVA_KEYWORDS or symbol!=unicodedata.normalize('NFC',symbol):failures.append(language+'/'+key+': invalid identifier')
            if symbol in used:failures.append(language+'/'+key+': duplicate identifier')
            used.add(symbol)
            if row['status']=='untranslated':missing.append(key)
            elif row.get('implementation_role_review')!='checked':unchecked.append(key)
            if re.search(r'_\d+$',symbol):collisions.append(key)
        languages[language]={'untranslated':missing,'role_review_pending':unchecked,'numeric_collision_suffixes':collisions,
            'native_review': 'pending','etymology_review':'pending','reviewed_roles':sum(r.get('implementation_role_review')=='checked' for r in rows.values()),
            'verified_lexeme_history':proof['languages'].get(language,{}).get('verified_lexeme_history',[])}
        for key in missing:pending.append((language,key,'translation-required'))
        for key in unchecked:pending.append((language,key,'implementation-context-and-language-review-required'))
    generated=json.loads((ROOT/'naming/generated-files.json').read_text());source_files=0
    for name,digest in generated.items():
        path=ROOT/name
        if not path.is_file() or path.is_symlink() or sha(path.read_bytes())!=digest:failures.append('Generated file mismatch: '+name)
    classes=[];arguments=[];samples=OUT/'examples';examples_count=0
    for index,edition in enumerate(editions):
        folder=ROOT/edition['path'];row=terms[edition['language']]
        if edition['identifiers']!={k:v['identifier'] for k,v in row.items()}:failures.append('Stale edition dictionary: '+edition['path'])
        for name in edition['sources']:
            path=folder/name;text=path.read_text();source_files+=1
            match=re.search(r'public\s+(?:final\s+|abstract\s+)?class\s+([^\s{]+)',text)
            if match is None or match.group(1)!=path.stem:failures.append('Class/file mismatch: '+str(path))
            arguments.append(path)
        if args.compile:
            name=edition['identifiers']['source']+'.java';example=folder/edition['examples']/name
            target=samples/str(index)/name;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text('package namingcheck.e'+str(index)+';\n'+example.read_text())
            arguments.append(target);examples_count+=1
    native_files=0;header_updates=0;native_editions=0;native_languages=set();untranslated_native={}
    if args.native:
        configs=sorted((ROOT/'country').glob('*/native.json'))+sorted((ROOT/'country').glob('*/*/native.json'))
        for index,config_path in enumerate(configs,1):
            folder=config_path.parent;config=json.loads(config_path.read_text());native_editions+=1;native_languages.add(config['language'])
            for field in ('builder','runner','image_builder','system_tester'):
                if field in config and not (folder/config['source']/config['native']/config[field]).is_file():failures.append('Missing native tool: '+str(folder)+'/'+field)
            manifest=folder/'native-generated.json';hashes=json.loads(manifest.read_text());changed=False
            untranslated_native[str(folder.relative_to(ROOT))]=config['naming']['untranslated_identifiers']
            for name,digest in list(hashes.items()):
                if not name.endswith('.java'):continue
                path=folder/name
                if not path.is_file() or path.is_symlink():failures.append('Missing or linked native Java: '+str(path));continue
                data=path.read_bytes();actual=sha(data);native_files+=1
                if path.stat().st_nlink!=1:failures.append('Shared native Java inode: '+str(path))
                if actual!=digest:
                    if args.record_copyright and matches_owned(data,digest):hashes[name]=actual;changed=True;header_updates+=1
                    else:failures.append('Native Java ownership mismatch: '+str(path))
                match=re.search(r'public\s+(?:final\s+|abstract\s+)?class\s+([^\s{]+)',data.decode())
                if match and match.group(1)!=path.stem:failures.append('Native class/file mismatch: '+str(path))
            if changed:dump(manifest,hashes)
            if index%100==0:print('Native Java inspected',index,flush=True)
    compiled=False
    if args.compile and not failures:
        classes=OUT/'classes';classes.mkdir(exist_ok=True)
        argfile=OUT/'javac-sources.txt';argfile.write_text('\n'.join('"'+str(path).replace('\\','\\\\').replace('"','\\"')+'"' for path in arguments)+'\n')
        subprocess.run(['javac','-J-XX:-UsePerfData','-J-Xmx2048m','--release','11','-encoding','UTF-8','-d',str(classes),'@'+str(argfile)],check=True)
        compiled=True
    report={'passed':not failures,'countries':len({e['country'] for e in editions}),'editions':len(editions),'languages':len({e['language'] for e in editions}),
        'generated_files_verified':len(generated),'linux_java_sources_checked':source_files,'linux_java_sources_compiled':source_files if compiled else 0,
        'examples_compiled':examples_count if compiled else 0,'native_editions_inspected':native_editions,'native_languages_inspected':len(native_languages),
        'native_java_files_inspected':native_files,'authorized_copyright_hashes_recorded':header_updates,
        'functional_roles_reviewed':sum(v['reviewed_roles'] for v in languages.values()),'language_details':languages,
        'native_untranslated_identifiers':untranslated_native,'native_speaker_review_complete':0,'all_language_etymologies_verified':False,
        'verified_lexeme_histories':sum(len(v['verified_lexeme_history']) for v in languages.values()),'failures':failures}
    dump(OUT/'audit.json',report)
    (OUT/'pending.tsv').write_text('language\tconcept\tstatus\n'+''.join('\t'.join(row)+'\n' for row in pending))
    print(json.dumps({k:v for k,v in report.items() if k not in ('language_details','native_untranslated_identifiers')},ensure_ascii=False,indent=2),flush=True)
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
