#!/usr/bin/env python3
"""All-country integrity + input/font coverage; all-language source compilation.

This is not a claim that every country's image has been boot-tested.
"""
import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unicodedata
from input import LocalInput
from generate import translate, translate_source
from java_prose import localize_java_comments
from commands import profile as command_profile, source as command_source
from naming_review import without_copyright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/native'


def sha(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda:stream.read(1024*1024),b''):digest.update(part)
    return digest.hexdigest()


def check_language(item):
    folder,config=item
    source=folder/config['source'];native=source/config['native'];mapping=config['identifiers']
    def local(path):return source/translate(path,mapping)
    report={'country':config['country'],'language':config['language'],'passed':False}
    try:
        for name in config['owned_files']:
            if name.endswith('.py'):ast.parse((source/name).read_text(),filename=name)
        p=json.loads((native/'input.json').read_text());buffer=['']
        def send(data):
            for char in data.decode('utf-8'):buffer[0]=buffer[0][:-1] if char=='\x7f' else buffer[0]+char
        if p['kind']=='hangul':
            path=native/config['runner'];tools=path.parent
            spec=importlib.util.spec_from_file_location('hangul_probe',str(tools/'한글입력.py'))
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);ime=module.한글조합(send)
        else:ime=LocalInput(send,p)
        for key in p['sample_keys']:
            if not ime.글쇠넣기(key):send(key.encode())
        assert buffer[0]==p['sample'],(buffer[0],p['sample'])
        report['input_sample']=buffer[0]
        bridge=subprocess.check_output([sys.executable,str(ROOT/'native/verify_input.py'),str(folder)],stderr=subprocess.STDOUT)
        report['input_bridge']=json.loads(bridge.decode('utf-8'))
        with tempfile.TemporaryDirectory(prefix='source-'+config['language']+'-',dir=str(OUT)) as temporary:
            temporary=Path(temporary);classes=temporary/'classes';classes.mkdir()
            library=list(local(config['native']+'/한국어자바').rglob('*.java'))
            examples=list((source/'example/java').glob('*.java'))
            command=['javac','-J-XX:-UsePerfData','--release','8','-encoding','UTF-8','-d',str(classes)]
            subprocess.check_output(command+[str(p) for p in library+examples],stderr=subprocess.STDOUT)
            report['java_library_and_examples']=len(library)+len(examples)
            core=list(local(config['native']+'/원문').glob('*.java'))
            bundle=temporary/(mapping.get('꾸러미','꾸러미')+'.java')
            bundle.write_text(translate('public final class 꾸러미 { public static void 준비() {} }',mapping))
            sample=temporary/(mapping.get('예제꾸러미','예제꾸러미')+'.java')
            sample.write_text(translate('public final class 예제꾸러미 { public static int 설치(int 언어) {return 0;} }',mapping))
            subprocess.check_output(command+[str(p) for p in core+[bundle,sample]],stderr=subprocess.STDOUT)
            shared=[p for p in local('os/사용자/자바').glob('*.java') if p.stem!=mapping.get('자바가상기계','자바가상기계')]
            users=list(local(config['native']+'/사용자/자바').glob('*.java'))
            subprocess.check_output(command+[str(p) for p in shared+users],stderr=subprocess.STDOUT)
            report['kernel_user_java']=len(core)+len(shared)+len(users)
            headers=local('posix-kor/arm64-native/포함')
            runtime_headers=local(config['native']+'/시언어번역기/개발규약')
            for example in (source/'example/c').glob('*.c'):
                subprocess.check_output(['clang','--target=aarch64-none-elf','-std=c11','-ffreestanding','-fsyntax-only','-I',str(headers),'-I',str(runtime_headers),str(example)],stderr=subprocess.STDOUT)
            report['c_examples']=4
            compiler=local('compiler/자바도구/기계어미리번역.java')
            launcher=next((folder/'native-java').glob('*.java'))
            subprocess.check_output(['javac','-J-XX:-UsePerfData','--release','11','-encoding','UTF-8',
                '-d',str(classes),str(compiler),str(launcher)],stderr=subprocess.STDOUT)
            report['java_host_tools']=2
        report['passed']=True
    except subprocess.CalledProcessError as error:report['error']=error.output.decode('utf-8','replace')
    except Exception as error:report['error']=repr(error)
    print(config['country'],config['language'],report['passed'],flush=True)
    if not report['passed']:print(report.get('error','Unknown failure'),flush=True)
    (OUT/('source-'+config['language']+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report={'passed':False,'countries':0,'languages':0,'files_verified':0,'source_compilation':[], 'untranslated_editions':[], 'unshaped_scripts':'Indic conjuncts and full bidi are not implemented', 'physical_pi_tested':False}
    representatives={};coverage=set(json.loads((ROOT/'native/resources/terminal-font.json').read_text())['coverage']);font_missing={}
    for path in sorted((ROOT/'country').glob('*/native.json')):
        config=json.loads(path.read_text());folder=path.parent;source=folder/config['source'];report['countries']+=1
        assert config['commands']==command_profile(config['language']),path
        command_path=source/config['native']/translate('원문/관리명령.java',config['identifiers'])
        expected=localize_java_comments('관리명령.java',translate_source('관리명령.java',command_source(config['language']),config['identifiers']),config['language'],config['identifiers'],config['native_name'])
        assert without_copyright(command_path.read_bytes()).decode()==expected,command_path
        manifest=json.loads((folder/'native-generated.json').read_text())
        for name,digest in manifest.items():
            target=folder/name
            assert str(target.resolve()).startswith(str(folder.resolve())+'/'),target
            assert sha(target)==digest,'Edited generated file: '+str(target)
            report['files_verified']+=1
        for name,key in [('native-vendor.tar.gz','vendor_sha256'),('qemu-host.tar.gz','qemu_sha256')]:assert sha(folder/name)==config[key],str(folder/name)
        assert (folder/'example').resolve()==source/'example'
        # The inherited RAM filesystem stores 63 UTF-8 path bytes and 16 KiB
        # per file. A translated name must fit in the guest, not just the host.
        for example in (source/'example').rglob('*'):
            if example.is_file():
                guest='/example/'+str(example.relative_to(source/'example'))
                assert len(guest.encode('utf-8'))<=63,guest
                assert example.stat().st_size<=16384,guest
        namespace=translate('한국어/자체/',config['identifiers'])
        library=source/config['native']/translate('한국어자바',config['identifiers'])
        for java in library.rglob('*.java'):
            resource=namespace+java.stem+'.class'
            assert len(resource.encode('utf-8'))<=511,resource
        representatives.setdefault(config['language'],(folder,config))
        if config['naming']['untranslated_identifiers']:report['untranslated_editions'].append(config['country'])
        sample=config['help']+config['input']['sample']+''.join(config['examples'].values())+''.join(config['commands']['aliases'].values())+''.join(config['commands']['descriptions'])
        missing=sorted({c for c in sample if not c.isspace() and unicodedata.category(c)[0] in 'LMN' and ord(c) not in coverage})
        if missing:font_missing[config['country']]=missing
    report['languages']=len(representatives);report['font_missing']=font_missing
    with ThreadPoolExecutor(max_workers=2) as pool:
        report['source_compilation']=list(pool.map(check_language,representatives.values()))
    report['passed']=not font_missing and all(r['passed'] for r in report['source_compilation'])
    (OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('COUNTRIES',report['countries'],'LANGUAGES',report['languages'],'PASS',report['passed'],flush=True)
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
