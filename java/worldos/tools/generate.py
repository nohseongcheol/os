#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET
from naming_review import COPYRIGHT, matches_owned, review
ROOT=Path(__file__).resolve().parents[1]
PENDING={}

def write(path,text,old,hashes):
    data=text.encode('utf-8') if isinstance(text,str) else text
    if path.suffix=='.java' and (ROOT/'templates/Demo.java').read_bytes().startswith(COPYRIGHT):
        data=COPYRIGHT+data.replace(COPYRIGHT,b'',1)
    relative=str(path.relative_to(ROOT))
    if path.name=='Makefile' and path.is_file() and '\n# WORLDOS_NATIVE_JAVA\n' in path.read_text():
        suffix=path.read_text().split('\n# WORLDOS_NATIVE_JAVA\n',1)[1]
        data+=('\n# WORLDOS_NATIVE_JAVA\n'+suffix).encode()
    if path.exists():
        current=hashlib.sha256(path.read_bytes()).hexdigest()
        if path.read_bytes()==data:
            hashes[relative]=current
            return
        if not matches_owned(path.read_bytes(),old.get(relative)):
            raise SystemExit('Preserving user edit; generation stopped: '+relative)
    PENDING[path]=data
    hashes[relative]=hashlib.sha256(data).hexdigest()

def main():
    terms=json.loads((ROOT/'naming/terms.json').read_text(encoding='utf-8'))
    concepts=json.loads((ROOT/'naming/concepts.json').read_text(encoding='utf-8'))
    inputs=json.loads((ROOT/'naming/input-methods.json').read_text(encoding='utf-8'))
    countries=json.loads((ROOT/'naming/countries.json').read_text())['3166-1']
    territories={x.get('type'):x for x in ET.parse(str(ROOT/'vendor/cldr48-supplementalData.xml')).findall('.//territoryInfo/territory')}
    previous=ROOT/'naming/generated-files.json';old=json.loads(previous.read_text()) if previous.exists() else {};hashes={};editions=[]
    templates={name:(ROOT/'templates'/name).read_text() for name in ['Workspace.java.in','FileAPI.java.in']}
    for country in sorted(countries,key=lambda x:x['alpha_3']):
        code=country['alpha_3'];territory=territories.get(country['alpha_2']);languages=list(territory) if territory is not None else []
        # Uninhabited territories / missing population data use an explicitly undetermined interface.
        if not languages: languages=[ET.Element('languagePopulation',{'type':'und','populationPercent':'0'})]
        for language in languages:
            lang=language.get('type');dictionary=terms.get(lang,terms['en']);symbols={k:v['identifier'] for k,v in dictionary.items()}
            root=ROOT/'country'/code/lang;package='worldos.'+code+'.l_'+lang.replace('-','_')
            sources=[]
            for template,key in [('Workspace.java.in','workspace'),('FileAPI.java.in','api')]:
                content=re.sub(r'__(\w+)__',lambda m:symbols[m.group(1)],templates[template])
                filename=symbols['source']+'/'+symbols[key]+'.java';sources.append(filename)
                write(root/filename,'package '+package+';\n'+content,old,hashes)
            labels={k:v['text'].replace('\n',' ') for k,v in dictionary.items()}
            labels.update(identity=code+'/'+lang,locale=lang.replace('_','-'),help='javac / java / jar / gcc · UTF-8 · '+package+'.'+symbols['api'])
            messagefile=symbols['messages']+'.properties'
            write(root/messagefile,''.join(k+'='+v.replace('\\','\\\\')+'\n' for k,v in sorted(labels.items())),old,hashes)
            examplefolder=symbols['directory']
            sample=re.sub(r'__(\w+)__',lambda m:symbols[m.group(1)],(ROOT/'templates/Demo.java').read_text())
            write(root/examplefolder/(symbols['source']+'.java'),sample,old,hashes)
            header='posix-'+code+'/'+symbols['api']+'.h'
            content='#pragma once\n#include <unistd.h>\n#include <fcntl.h>\n#include <sys/stat.h>\n#include <sys/socket.h>\n#include <pthread.h>\n'
            for key,standard in [('open','open'),('read','read'),('write','write'),('close','close'),('seek','lseek'),('sync','fsync'),('remove','unlink'),('connect','connect')]:
                if symbols[key]!=standard:content+='#define '+symbols[key]+' '+standard+'\n'
            write(root/header,content,old,hashes)
            missing=[k for k,v in dictionary.items() if v['status']=='untranslated']
            if lang=='und':missing=list(dictionary)
            info={'country':code,'country_alpha2':country['alpha_2'],'country_name':country['name'],'language':lang,
                  'official_status':language.get('officialStatus','population-listed'),'population_percent':language.get('populationPercent'),
                  'main':package+'.'+symbols['workspace'],'sources':sources,'messages':messagefile,'examples':examplefolder,'posix':header,'identifiers':symbols,
                  'untranslated':missing,'native_review':'pending','independent_sources':True,'runtime':'Linux / Alpine 3.24 / OpenJDK 25'}
            info['input_method']=inputs.get(lang,{'engine':'keyboard-us','source':'Fallback','review':'pending'})
            write(root/'edition.json',json.dumps(info,ensure_ascii=False,indent=2)+'\n',old,hashes)
            write(root/(symbols['name']+'.json'),json.dumps(dictionary,ensure_ascii=False,indent=2)+'\n',old,hashes)
            write(root/(symbols['label']+'.json'),json.dumps(concepts,ensure_ascii=False,indent=2)+'\n',old,hashes)
            for tool in ['edition.py','archive.py','ip_config.py']:write(root/tool,(ROOT/'tools'/tool).read_bytes(),old,hashes)
            write(root/'Makefile','PYTHON ?= python3\n.PHONY: build run\nbuild:\n\t$(PYTHON) edition.py build\nrun:\n\t$(PYTHON) edition.py run\n'
                  '\n.PHONY: clean\nclean:\n'
                  '\t# Keep the persistent guest data disk and its lock.\n'
                  '\t@if test -d build; then \\\n'
                  '\t\tfind build -mindepth 1 -maxdepth 1 ! -name data.ext4 ! -name data.ext4.lock -exec rm -rf -- {} +; \\\n'
                  '\tfi\n',old,hashes)
            editions.append(dict(info,path=str(root.relative_to(ROOT))))
    # Preflight every destination before changing any edition source.
    for path,data in PENDING.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
        native_manifest=path.parent/'native-generated.json'
        if path.name=='Makefile' and native_manifest.is_file():
            native_hashes=json.loads(native_manifest.read_text());native_hashes['Makefile']=hashlib.sha256(data).hexdigest()
            native_manifest.write_text(json.dumps(native_hashes,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'editions.json').write_text(json.dumps(editions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for relative,digest in old.items():
        path=ROOT/relative
        if relative not in hashes and path.is_file() and matches_owned(path.read_bytes(),digest):
            path.unlink()
    previous.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={'countries':len(countries),'editions':len(editions),'languages':len({e['language'] for e in editions}),
            'editions_without_english_fallback':sum(not e['untranslated'] for e in editions),'native_review_complete':0,
            'source':'CLDR 48 territoryInfo, all listed languages; ISO 3166-1 countries and territories'}
    reviewed=review()
    report.update(functional_review_languages=len(reviewed['languages']),
                  functional_roles_reviewed=sum(len(v['terms']) for v in reviewed['languages'].values()),
                  untranslated_concepts=sum(v['status']=='untranslated' for rows in terms.values() for v in rows.values()),
                  all_language_etymologies_verified=False)
    (ROOT/'naming/coverage.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
