#!/usr/bin/env python3
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile
ROOT=Path(__file__).resolve().parents[1]

def build_all(editions):
    output=ROOT/'build/all';output.mkdir(parents=True,exist_ok=True)
    # Different edition packages permit one compiler invocation without source sharing.
    for start in range(0,len(editions),80):
        group=editions[start:start+80]
        batch=output/str(start);batch.mkdir(exist_ok=True)
        arguments=batch/'sources.args'
        paths=[ROOT/e['path']/source for e in group for source in e['sources']]
        arguments.write_text('\n'.join('"'+str(p)+'"' for p in paths)+'\n',encoding='utf-8')
        subprocess.run(['javac','-J-Xmx1024m','--release','11','-encoding','UTF-8','-d',str(batch),'@'+str(arguments)],check=True)
        for edition in group:
            root=ROOT/edition['path'];destination=root/'build';destination.mkdir(exist_ok=True)
            package=edition['main'].rsplit('.',1)[0].replace('.','/')
            with zipfile.ZipFile(str(destination/'edition.jar.next'),'w',zipfile.ZIP_DEFLATED) as archive:
                archive.writestr('META-INF/MANIFEST.MF','Manifest-Version: 1.0\r\nMain-Class: '+edition['main']+'\r\n\r\n')
                for source in (batch/package).glob('*.class'):archive.write(str(source),str(source.relative_to(batch)))
                archive.write(str(root/edition['messages']),'messages.properties')
            (destination/'edition.jar.next').replace(destination/'edition.jar')
        print('Compiled editions: '+str(min(start+80,len(editions)))+'/'+str(len(editions)),flush=True)
    report={'compiled_editions':len(editions),'failed':0,'compiler':subprocess.check_output(['javac','-version'],stderr=subprocess.STDOUT).decode().strip()}
    (ROOT/'build/build-report.json').write_text(json.dumps(report,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser(description='Independent WorldOS country/language editions')
    parser.add_argument('command',choices=['list','build-all','build','run','export'])
    parser.add_argument('edition',nargs='?',default='KOR/ko');parser.add_argument('--output');parser.add_argument('--headless',action='store_true')
    args,rest=parser.parse_known_args();editions=json.loads((ROOT/'editions.json').read_text(encoding='utf-8'))
    if args.command=='list':
        for e in editions:print(e['country']+'/'+e['language']+'\t'+e['official_status']+'\tuntranslated='+str(len(e['untranslated'])))
        return
    if args.command=='build-all':return build_all(editions)
    matched=[e for e in editions if e['country']+'/'+e['language']==args.edition]
    if not matched:raise SystemExit('Unknown edition; use make list')
    edition=matched[0];root=ROOT/edition['path']
    if args.command=='export':
        if not args.output:raise SystemExit('--output is required for export')
        destination=Path(args.output).resolve()
        if destination.exists():raise SystemExit('Export destination already exists; choose a new directory')
        shutil.copytree(str(root),str(destination),ignore=shutil.ignore_patterns('build','*.lock','__pycache__'))
        from ip_config import read_config
        config = read_config(root)
        (destination/'ip.conf').write_text(''.join(key+'='+config[key]+'\n' for key in ('IP','NETMASK','GATEWAY','DNS')))
        shutil.copytree(str(ROOT/'build/runtime'),str(destination/'runtime'),ignore=shutil.ignore_patterns('base.cpio'))
        shutil.copytree(str(ROOT/'docs'),str(destination/'docs'))
        print('Independent edition exported: '+str(destination));return
    command=['python3',str(root/'edition.py'),args.command]
    if args.headless:command.append('--headless')
    subprocess.run(command+rest,check=True)
if __name__=='__main__':main()
