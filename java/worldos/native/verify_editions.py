#!/usr/bin/env python3
"""모든 언어판의 원문·독립 파일·기능 포함을 검사하고 고유 Java 도구를 컴파일한다."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from generate import sources, translate

ROOT=Path(__file__).resolve().parents[1]

def compilation_form(data):
    # Localized banners are string values; they do not change Java types or
    # identifiers. Keep Unicode escapes and every character literal intact.
    text=data.decode('utf-8')
    pattern=re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
    def replace(match):
        value=match.group()
        return '""' if value.startswith('"') and '\\u' not in value else value
    return pattern.sub(replace,text).encode()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def compile_tools(item):
    fingerprint,group=item
    with tempfile.TemporaryDirectory(prefix='worldos-java-tools-') as temporary:
        destination=Path(temporary)
        command=['javac','-J-XX:-UsePerfData','--release','11','-encoding','UTF-8','-d',temporary]
        subprocess.check_output(command+[str(p) for p in group['host']],stderr=subprocess.STDOUT)
        mapping=group['mapping']
        bundle=destination/(mapping.get('꾸러미','꾸러미')+'.java')
        bundle.write_text(translate('public final class 꾸러미 { public static void 준비() {} }',mapping))
        examples=destination/(mapping.get('예제꾸러미','예제꾸러미')+'.java')
        examples.write_text(translate('public final class 예제꾸러미 { public static int 설치(int 언어) {return 0;} }',mapping))
        application_sources=group['core']+[bundle,examples]+group['library']+group['user']+group['managed']+group['jdk_library']
        subprocess.check_output(command+[str(p) for p in application_sources],stderr=subprocess.STDOUT)
        subprocess.check_output(command+[str(p) for p in group['x86_core']],stderr=subprocess.STDOUT)
    print('Java tools OK',fingerprint[:12],flush=True)
    return fingerprint

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse-exact-log',type=Path,help='Successful exact-source compilation log from this source snapshot')
    parser.add_argument('--reuse-structure-log',type=Path,help='Successful compilation-form log from this source snapshot')
    parser.add_argument('--jobs',type=int,default=2,choices=range(1,9))
    args=parser.parse_args()
    baseline=sources();h=hashlib.sha256()
    for name,data in sorted(baseline.items()):h.update(name.encode());h.update(data)
    expected=h.hexdigest();editions=json.loads((ROOT/'editions.json').read_text());files=0;unique={};languages=set();cached=set()
    prior=set(re.findall(r'Java tools OK ([0-9a-f]{12})',args.reuse_exact_log.read_text())) if args.reuse_exact_log else set()
    prior_structures=set(re.findall(r'Java tools OK ([0-9a-f]{12})',args.reuse_structure_log.read_text())) if args.reuse_structure_log else set()
    for number,edition in enumerate(editions,1):
        folder=ROOT/edition['path'];config=json.loads((folder/'native.json').read_text());source=folder/config['source']
        assert config['upstream_source_sha256']==expected,folder
        assert {translate(name,config['identifiers']) for name in baseline}<=set(config['owned_files']),folder
        for name in baseline:
            path=source/translate(name,config['identifiers'])
            assert path.is_file() and not path.is_symlink() and path.stat().st_nlink==1,path
        for name,sha in json.loads((folder/'native-generated.json').read_text()).items():
            path=folder/name
            assert path.is_file() and not path.is_symlink() and digest(path)==sha,path
            files+=1
        resource=folder/config.get('resource_root','.')
        for name,key in [('native-vendor.tar.gz','vendor_sha256'),('qemu-host.tar.gz','qemu_sha256')]:
            archive=resource/name
            assert archive.is_file() and not archive.is_symlink() and archive.stat().st_nlink==1,archive
        compiler=source/translate('compiler/자바도구/기계어미리번역.java',config['identifiers'])
        launcher=next((folder/'native-java').glob('*.java'))
        mapping=config['identifiers']
        def local(name):return source/translate(name,mapping)
        group={'host':[compiler,launcher], 'mapping':mapping,
            'core':list(local(config['native']+'/원문').glob('*.java')),
            'library':list(local(config['native']+'/한국어자바').rglob('*.java')),
            'user':[p for p in local('os/사용자/자바').glob('*.java') if p.stem!=mapping.get('자바가상기계','자바가상기계')]+list(local(config['native']+'/사용자/자바').glob('*.java')),
            'managed':list(local('원천').rglob('*.java')),
            'jdk_library':list(local('한국어자바/원문').rglob('*.java')),
            'x86_core':list(local('os/원문').glob('*.java'))}
        contents=[p.read_bytes() for key in ('host','core','library','user','managed','jdk_library','x86_core') for p in sorted(group[key])]
        raw=hashlib.sha256(b''.join(contents)).hexdigest()
        fingerprint=hashlib.sha256(b''.join(compilation_form(data) for data in contents)).hexdigest()
        if raw[:12] in prior or fingerprint[:12] in prior_structures:cached.add(fingerprint)
        unique.setdefault(fingerprint,group);languages.add(config['language'])
        if number%100==0:print('Integrity',edition['path'],flush=True)
    print('Compilation groups',len(unique),'previously compiled',len(cached),flush=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:compiled=list(pool.map(compile_tools,[(key,value) for key,value in unique.items() if key not in cached]))
    report={'passed':True,'editions':len(editions),'languages':len(languages),'files_verified':files,
        'upstream_source_sha256':expected,'unique_java_source_structures_verified':len(unique),
        'previously_compiled_structures':len(cached),'additional_structures_compiled':len(compiled),
        'message_literal_variants_reused':True,'unicode_escapes_and_character_literals_preserved':True,'all_languages_boot_tested':False,
        'translation_and_etymology_review':'pending'}
    (ROOT/'build/native/all-edition-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
