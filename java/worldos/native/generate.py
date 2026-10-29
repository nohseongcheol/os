#!/usr/bin/env python3
"""Generate independently editable native country trees, preserving old editions."""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tarfile
import tokenize
import sys
from functools import lru_cache
from archives import archive_writer, copy_archive, publish_archive
from paths import jkoros_root
from resources import keyboard, phonetic, write_json, OUTPUT
from terms import names, HELP, GREETINGS, LAYOUTS
from identifier_rules import source as identifier_source
from commands import profile as command_profile, source as command_source, KEYS as COMMAND_KEYS
sys.path.append(str(Path(__file__).resolve().parents[1]/'tools'))
from naming_review import COPYRIGHT, matches_owned
from source_names import rename_source, make_renamer
from java_prose import localize_java_comments

ROOT=Path(__file__).resolve().parents[1]
JKOROS=jkoros_root()
NATIVE='platforms/rpi4-native'
TOKEN=re.compile(r'[\w$]+',re.UNICODE)
SKIP={'build','dist','__pycache__','.git','.vbox','vendor'}
TRANSLATED={}
LEGACY_HASHES={}
UPDATED_LEGACY={}


@lru_cache(maxsize=128)
def translator(items):
    return make_renamer(dict(items))


def translate(text, mapping):
    return translator(tuple(mapping.items()))(text)


def translate_source(path, text, mapping):
    return rename_source(path, text, translator(tuple(mapping.items())))


def sources():
    result={}
    for base in [JKOROS/NATIVE,JKOROS/'compiler',JKOROS/'os',JKOROS/'posix-kor',JKOROS/'example',
                 JKOROS/'원천',JKOROS/'한국어자바',JKOROS/'도구',JKOROS/'src',JKOROS/'docs',JKOROS/'문서',
                 JKOROS/'distribution',JKOROS/'platforms/rpi4']:
        for directory,folders,files in os.walk(str(base)):
            folders[:]=sorted(f for f in folders if f not in SKIP)
            for name in sorted(files):
                path=Path(directory)/name
                if path.is_symlink() or path.suffix in ('.pyc','.class','.o','.elf','.img','.a','.bak'):continue
                result[str(path.relative_to(JKOROS))]=path.read_bytes()
    for name in ['LICENSE','THIRD_PARTY_NOTICES.md','Makefile','만들기.mk','안내.md','pack.sh','unpack.sh','ip.conf']:
        result[name]=(JKOROS/name).read_bytes()
    return result


def identifiers(path,text):
    if path.endswith('.py'):
        try:return [token.string for token in tokenize.generate_tokens(io.StringIO(text).readline) if token.type==tokenize.NAME]
        except tokenize.TokenError:return []
    if Path(path).suffix not in ('.java','.c','.h','.cpp'):return []
    code=re.sub(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', text, flags=re.S)
    return TOKEN.findall(code)


@lru_cache(maxsize=None)
def archive_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vendor_bundle():
    target=OUTPUT/'native-vendor.tar.gz'
    with archive_writer(target) as temporary, tarfile.open(str(temporary),'w:gz') as archive:
        base=JKOROS/NATIVE/'vendor'
        for path in sorted(base.rglob('*')):
            if not path.is_file():continue
            name=NATIVE+'/vendor/'+str(path.relative_to(base))
            replacement=OUTPUT/path.name if path.name in ('terminal-font.bin','terminal-font.json') else path
            data=replacement.read_bytes();info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644
            archive.addfile(info,io.BytesIO(data))
        sdk=JKOROS/'platforms/rpi4/build/rootfs'
        headers=list((sdk/'usr/include').glob('*.h'))
        headers+=list((sdk/'usr/include/bits').rglob('*.h'))+list((sdk/'usr/include/sys').rglob('*.h'))
        for path in headers+sorted((sdk/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a')):
            data=path.read_bytes();info=tarfile.TarInfo(NATIVE+'/vendor/sdk/'+str(path.relative_to(sdk)))
            info.size=len(data);info.mode=0o644;archive.addfile(info,io.BytesIO(data))
        firmware=io.BytesIO()
        with tarfile.open(str(JKOROS/'platforms/rpi4/vendor/alpine-rpi-3.24.2-aarch64.tar.gz')) as source, tarfile.open(fileobj=firmware,mode='w:gz') as dest:
            for name in ('start4.elf','fixup4.dat','bcm2711-rpi-4-b.dtb','overlays/disable-bt.dtbo'):
                member=source.getmember('./'+name);data=source.extractfile(member).read()
                info=tarfile.TarInfo('./'+name);info.size=len(data);info.mode=0o644;dest.addfile(info,io.BytesIO(data))
        for name,data in [('pi4-firmware.tar.gz',firmware.getvalue()),('pi4-firmware.tar.gz.sha256',(hashlib.sha256(firmware.getvalue()).hexdigest()+'  pi4-firmware.tar.gz\n').encode())]:
            info=tarfile.TarInfo(NATIVE+'/vendor/'+name);info.size=len(data);archive.addfile(info,io.BytesIO(data))
        for path in [Path('/usr/share/doc/xkb-data/copyright'),Path('/usr/share/common-licenses/LGPL-2.1')]:
            data=path.read_bytes();info=tarfile.TarInfo(NATIVE+'/vendor/input-licenses/'+path.parent.name+'-'+path.name);info.size=len(data);archive.addfile(info,io.BytesIO(data))
        for name in ('ja-anthy.mim','zh-py.mim','am-sera.mim'):
            data=(ROOT/'build/rootfs/usr/share/m17n'/name).read_bytes();info=tarfile.TarInfo(NATIVE+'/vendor/input-sources/'+name);info.size=len(data);archive.addfile(info,io.BytesIO(data))
        for relative, data in {
            'LICENSE.worldos-fonts':'Noto fonts: SIL Open Font License 1.1, https://github.com/notofonts\nDejaVu: see LICENSE.fonts-dejavu-core.\nSource font hashes: terminal-font.json.\n',
        }.items():
            raw=data.encode();info=tarfile.TarInfo(NATIVE+'/vendor/'+relative);info.size=len(raw);archive.addfile(info,io.BytesIO(raw))
    return target


def profile(language):
    if language == 'zh':
        return json.loads((ROOT / 'native/inputs/zh-default-input.json').read_text())
    if language=='ko':return {'kind':'hangul','source':'jkoros two-set Hangul composer','sample_keys':'gksrmf','sample':'한글'}
    if language=='ja':
        result=phonetic('ja-anthy.mim','kana');result.update(sample_keys='nihongo',sample='にほんご',limitations='Kana composition; no Anthy dictionary conversion. Unicode paste accepts Kanji.')
        return result
    if language in ('zh_Hans','zh_Hant'):
        # Both scripts are available in the upstream Unihan candidate table.
        result=phonetic('zh-py.mim','candidates');result.update(sample_keys='ni',sample='你',limitations='Syllable candidates: Space cycles, F9 commits. No predictive phrase model.')
        charset='big5' if language=='zh_Hant' else 'gb2312'
        def supported(char):
            try:char.encode(charset);return True
            except UnicodeEncodeError:return False
        result['map']={key:[c for c in value if supported(c)] for key,value in result['map'].items() if isinstance(value,list)}
        result['map']={key:value for key,value in result['map'].items() if value}
        result['candidate_charset']=charset
        result['map']['ni'].remove('你');result['map']['ni'].insert(0,'你')
        return result
    if language in ('am','ti'):
        result=phonetic('am-sera.mim','phonetic');result.update(sample_keys='se',sample='ሰ');return result
    layout,variant=LAYOUTS.get(language,('us','altgr-intl' if language not in ('en','und') else ''))
    result=keyboard(layout,variant)
    result['fallback']=language not in LAYOUTS and language not in ('en','und','id','ms_Latn','sw','so','sm','to','tvl','tpi','bi','pau','pap','mg','rn','rw','sn','st','wo','ht')
    # Test a non-ASCII native key where one exists; US is intentional for many
    # Latin orthographies. AltGr and dead-key tables are retained separately.
    key=next((k for k,v in result['map'].items() if any(ord(c)>127 for c in v) and not v.startswith('dead:')),'a')
    result.update(sample_keys=key,sample=result['map'].get(key,key))
    return result


def adapt(base,language,native_name,input_profile):
    result=dict(base)
    from localization_runtime import PATCHES, update
    for path, edits in PATCHES.items():
        result[path] = update(result[path].decode('utf-8'), edits).encode('utf-8')
    if language!='ko':result['도구/한글이름검사.sh']=(ROOT/'native/inputs/localized-audit.sh').read_bytes()
    result[NATIVE+'/원문/관리명령.java']=command_source(language).encode()
    compiler='os/사용자/자바/자바컴파일러.java'
    text=result[compiler].decode()
    text=re.sub(r'    static boolean 글자\(int 값\) \{.*?\n    }', '    static boolean 글자(int 값) { return 문자이름규칙.첫글자(값); }', text,flags=re.S)
    text=text.replace('(글자(원문[수]) || 숫자(원문[수]))','문자이름규칙.이어진글자(원문[수])')
    result[compiler]=text.encode()
    result['os/사용자/자바/문자이름규칙.java']=identifier_source().encode()
    program='os/사용자/프로그램.mk'
    result[program]=result[program].decode().replace('사용자/자바/자바컴파일러.java','사용자/자바/자바컴파일러.java 사용자/자바/문자이름규칙.java').encode()
    def edit(path,change):result[NATIVE+'/'+path]=change(result[NATIVE+'/'+path].decode()).encode()
    edit('도구/자바라이브러리빌드.py',lambda t:t if "(기준경로 / 'build/user').mkdir" in t else t.replace("    출력결과 = 기준경로 / 'build/java-library'", "    (기준경로 / 'build/user').mkdir(parents=True, exist_ok=True)\n    출력결과 = 기준경로 / 'build/java-library'"))
    edit('도구/시언어번역기빌드.py',lambda t:t.replace("기준경로.parent / 'rpi4/build/rootfs'", "기준경로 / 'vendor/sdk'"))
    edit('도구/영상만들기.py',lambda t:t.replace("기준.parent / 'rpi4/vendor/alpine-rpi-3.24.2-aarch64.tar.gz'", "기준 / 'vendor/pi4-firmware.tar.gz'"))
    edit('파이썬연결/Makefile',lambda t:t.replace('-std=gnu99','-std=gnu11'))
    help_text=HELP.get(language,'F9 / Shift+Space: [EN] ↔ ['+native_name+']')
    if language=='zh_Hant':help_text='按 F9 或 Shift+Space 可切換到中文拼音輸入。'
    details=[help_text,'  ['+language.upper()+'] '+input_profile['kind']+'; [EN] ASCII',
             '  '+input_profile['sample_keys']+' → '+input_profile['sample'],
             '  F9: EN ↔ '+native_name+' | Ctrl+Shift+V: UTF-8',
             '  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr',
             '  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal']
    if input_profile['kind']=='candidates':details.append('  Space: next candidate; F9: commit / EN')
    if input_profile.get('limitations'):details.append('  '+input_profile['limitations'])
    body='    static void 한글도움말() {\n'+''.join('        단말.쓰기('+json.dumps(line+'\n',ensure_ascii=False)+');\n' for line in details)+'    }\n'
    edit('원문/명령해석기.java',lambda t:re.sub(r'    static void 한글도움말\(\) \{.*?\n    }\n',lambda _:body,t,flags=re.S).replace('같음(1, "ko")','같음(1, "ko") || 같음(1, "input")').replace('한글 터미널',native_name+' terminal'))
    greeting=GREETINGS.get(language,native_name)
    edit('원문/핵심.java',lambda t:t.replace('자체 Java 커널 · 안녕하세요 · 日本語 · العربية · 😀','WorldOS '+language+' · '+greeting+' · 😀'))
    # UTF-8 labels, unlike the old byte-at-a-time title renderer.
    title='static void 이름표(unsigned 가로좌표,unsigned 세로좌표,const char *문자열값,unsigned 전경색,unsigned 배경색){while(*문자열값){unsigned 문자값=(unsigned char)*문자열값++, 남은수=0;if(문자값>=0xc0){남은수=문자값<0xe0?1:문자값<0xf0?2:3;문자값&=(1u<<(6-남은수))-1;while(남은수--&&*문자열값)문자값=(문자값<<6)|((unsigned char)*문자열값++&63);}터미널글자그림(가로좌표,세로좌표,문자값,전경색,배경색);가로좌표+=넓은글자(문자값)*8;}}'
    edit('기계/터미널.c',lambda t:re.sub(r'static void 이름표\([^\n]+',lambda _:title,t).replace('[KO]','['+language.split('_')[0].upper()+']'))
    def bridge(text):
        text=text.replace('from 한글입력 import 한글조합','from local_input import create').replace('한글조합(보내기)','create(보내기, Path(__file__).resolve().parents[1])').replace('65<=글자부호<=122','32<=글자부호<127')
        text=text.replace('자신.입력방식알림 = 입력방식알림','자신.유니코드입력 = None\n        자신.입력방식알림 = 입력방식알림')
        text=text.replace('(0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea)', '(0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e)')
        text=text.replace('        if 글쇠기호 in (0xff31,0xffc6)', '''        if 제어글쇠 and 윗글쇠 and 글쇠기호 in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if 글쇠기호 in (32,0xff0d):
                try:
                    값=int(자신.유니코드입력,16)
                    if 32<=값<=0x10ffff and not 0xd800<=값<=0xdfff: 자신.보내기(chr(값).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif 글쇠기호==0xff1b: 자신.유니코드입력=None
            elif 글쇠기호==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif 글쇠기호<128 and chr(글쇠기호) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(글쇠기호)
            return
        if 글쇠기호 in (0xff31,0xffc6)''')
        text=text.replace("        앞부분 = b'\\x1b' if 자신.보조글쇠 & {0xffe9, 0xffea} else b''", "        if 자신.한글여부 and 자신.보조글쇠 & {0xffea,0xfe03,0xff7e} and not 제어글쇠 and hasattr(자신.한글조합기, 'profile'):\n            if 자신.한글조합기.글쇠넣기(chr(글자부호), altgr=True): return\n        앞부분 = b'\\x1b' if 자신.보조글쇠 & {0xffe9, 0xffea} else b''")
        return text
    edit('도구/바탕화면.py',bridge)
    result[NATIVE+'/도구/local_input.py']=(ROOT/'native/input.py').read_bytes()
    result[NATIVE+'/input.json']=(json.dumps(input_profile,ensure_ascii=False,indent=2)+'\n').encode()
    for path in list(result):
        if path.startswith('example/'):
            text=result[path].decode()
            # Replace user-facing sentences separately from identifier proposals.
            replacements={'안녕하세요':greeting,'한글 자료':native_name,'한글':native_name,
                '한국어 Swing 인사':native_name+' Swing','이름을 적고 인사하기를 누르세요.':greeting,
                '아직 인사하지 않았습니다.':greeting,'한/영: F9 또는 Shift+Space | 닫기: X':'F9 / Shift+Space | X',
                '누리':native_name,'그림을 확인한 뒤 Enter를 누르세요.':'Enter', '빨강 초록 파랑':'RGB'}
            for old,new in sorted(replacements.items(),key=lambda x:-len(x[0])):text=text.replace(old,new)
            result[path]=text.encode()
    # Compact guest manual, within the RAM file limit.
    result['example/README.md']=('\n'.join(['WorldOS '+language+' / '+native_name,help_text,'',
        'example java | example c | example python','cd /example/java','javac 출력예제.java','java 출력예제',
        'java 창예제','vi 출력예제.java','', 'cd /example/c','cc 출력예제.c -o demo','./demo',
        'cd /example/python','python 출력예제.py','','TCP/UDP: --network; FTP: ftpd start',
        'RAM files: 64 × 16 KiB; not persistent.','Native subset JVM / MicroPython / TinyCC; not full OpenJDK or Linux.'])+'\n').encode()
    return result,help_text


def generate(row,base,vendor,host,inputs,edition=None):
    code=row['country_alpha3'];language=row['language'];native_name=row['native_name']
    if language == 'zh': native_name = '中文'
    folder=ROOT/'country'/code if edition is None else ROOT/edition['path']
    layout=json.loads((ROOT/'native/inputs/country-layouts.json').read_text())[code]
    source_name=layout['paths']['소스'] if edition is None else 'native-source'
    from country_naming import names_for_country, country_source_identity
    mapping=names_for_country(code,language)
    # Country namespaces differ even when the edition language is shared.
    # Reuse translation work, while still writing independent files and checking
    # every country's existing files before replacement.
    cache_key=(code,language,native_name)
    if cache_key not in TRANSLATED:
        if len(TRANSLATED)>=12:TRANSLATED.clear()
        local,help_text=adapt(base,language,native_name,inputs[language])
        translated={};paths={};untranslated=set();count=0
        for old,data in local.items():
            name=translate(old,mapping);paths[old]=name
            try:
                text=data.decode('utf-8')
                tokens=identifiers(old,text);untranslated.update(token for token in tokens if any('\uac00'<=c<='\ud7a3' for c in token) and token not in mapping)
                count+=sum(1 for token in tokens if token in mapping)
                data=localize_java_comments(old,country_source_identity(old,translate_source(old,text,mapping),mapping),language,mapping,native_name).encode()
                if old == NATIVE + '/원문/명령해석기.java':
                    from localization_runtime import repair_input_help
                    data = repair_input_help(data.decode('utf-8'), mapping, help_text).encode('utf-8')
            except UnicodeDecodeError:pass
            if name in translated:
                raise ValueError('Localized source path collision: ' + name)
            translated[name]=data
        TRANSLATED[cache_key]=(translated,paths,untranslated,count,help_text)
    translated,paths,untranslated,count,help_text=TRANSLATED[cache_key]
    untranslated = set(untranslated)
    launcher_source = (ROOT / 'native/국가실행기.java').read_text()
    if language != 'ko':
        untranslated.update(t for t in identifiers('launcher.java', launcher_source)
                            if any('\uac00' <= c <= '\ud7a3' for c in t) and t not in mapping)
    pending={source_name+'/'+name:data for name,data in translated.items()};owned=list(translated)
    # Examples are real files within the standalone source tree, exposed by a
    # relative in-tree link at the country root for convenient discovery.
    config={'version':1,'country':code,'language':language,'native_name':native_name,
        'source':source_name,'native':NATIVE,'builder':translate('도구/빌드.py',mapping),
        'runner':translate('도구/실행.py',mapping),'image_builder':translate('도구/영상만들기.py',mapping),
        'vendor_sha256':archive_digest(vendor),
        'qemu_sha256':archive_digest(host),
        'owned_files':owned,'help':help_text,'help_sentence_translated':language in HELP,'identifiers':mapping,
        'commands':command_profile(language),
        'ip_configuration':{'file':'ip.conf','default_ip':'192.168.0.100','loaded_at':'build','shared_worldos_file':True},
        'system_tester':translate('도구/체계도구시험.py',mapping),
        'naming':{'mapped_identifiers':len(mapping),'replaced_occurrences':count,'untranslated_identifiers':len(untranslated) if language!='ko' else 0,'native_review':'pending','etymology_review':'pending'},
        'input':{k:v for k,v in inputs[language].items() if k not in ('map','altgr')},
        'kernel':mapping['제이코로스']+' own Java AOT ARM64 EL1; not Linux','full_openjdk':False,
        'examples':{Path(k).stem:Path(v).stem for k,v in paths.items() if k.startswith('example/java/') and k.endswith('.java')}}
    upstream=hashlib.sha256()
    for name,data in sorted(base.items()):upstream.update(name.encode());upstream.update(data)
    config['upstream_source_sha256']=upstream.hexdigest()
    config['java_migration']={'arm64_aot':'Java','x86_aot':'Java','framebuffer_composition':'Java',
        'remaining_python':'build, download, distribution, tests and compatibility readers',
        'remaining_c':'hardware and ABI bridges, terminal/widgets, network/FTP, external libraries',
        'complete':False}
    from country_naming import validate_edition
    config['country_naming'] = validate_edition(folder, config)
    pending['native.json']=(json.dumps(config,ensure_ascii=False,indent=2)+'\n').encode()
    if edition is not None:
        config['resource_root']='..'
        pending['native.json']=(json.dumps(config,ensure_ascii=False,indent=2)+'\n').encode()
    pending['native-commands.json']=(json.dumps(config['commands'],ensure_ascii=False,indent=2)+'\n').encode()
    pending['native-edition.py']=(ROOT/'native/edition.py').read_bytes()
    launcher_name=mapping.get('국가실행기','국가실행기')+'.java'
    pending['native-java/'+launcher_name]=localize_java_comments('launcher.java',translate_source('launcher.java',launcher_source,mapping),language,mapping,native_name).encode()
    pending['native-launch.sh']=('#!/bin/sh\nset -eu\nedition_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)\nexec java -XX:-UsePerfData "-Dworldos.edition.root=$edition_root" "$edition_root/native-java/'+launcher_name+'" "$@"\n').encode()
    pending['Makefile']=b'PYTHON ?= python3\nRESOLUTION ?= 1920x1080\nARGS ?=\n.PHONY: all build run desktop image check\nall: build\nbuild:\n\t$(PYTHON) native-edition.py build\nrun:\n\t$(PYTHON) native-edition.py run --resolution $(RESOLUTION) $(ARGS)\ndesktop:\n\t$(PYTHON) native-edition.py desktop --resolution $(RESOLUTION) $(ARGS)\nimage:\n\t$(PYTHON) native-edition.py image --resolution $(RESOLUTION) $(ARGS)\ncheck:\n\t$(PYTHON) native-edition.py check\n'
    pending['Makefile']+=b'.PHONY: test-system\ntest-system:\n\t$(PYTHON) native-edition.py test-system $(ARGS)\n'
    pending['Makefile']+=('\n.PHONY: x86-build x86-iso\nx86-build:\n\t$(MAKE) -C "'+source_name+'/os"\nx86-iso:\n\t$(MAKE) -C "'+source_name+'/os" iso\n').encode()
    pending['Makefile']+=('\n.PHONY: clean\nclean:\n'
        '\t$(MAKE) -C "'+source_name+'" clean\n'
        '\t@set -e; for makefile in $(wildcard */Makefile); do \\\n'
        '\t\t$(MAKE) -C "$${makefile%/Makefile}" clean; \\\n'
        '\tdone\n').encode('utf-8')
    pending['Makefile']=pending['Makefile'].replace(b'$(PYTHON) native-edition.py',b'sh native-launch.sh')
    if edition is not None:pending['native.mk']=pending.pop('Makefile')
    if edition is not None:
        makefile=folder/'Makefile'
        original=makefile.read_bytes()
        marker=b'\n# WORLDOS_NATIVE_JAVA\n'
        original=original.split(marker,1)[0]
        if marker not in original:
            original+=marker+b'.PHONY: native-build native-run native-desktop native-image native-check native-clean native-x86-iso\n'
            original+=b'native-build:\n\t$(MAKE) -f native.mk build\nnative-run:\n\t$(MAKE) -f native.mk run\nnative-desktop:\n\t$(MAKE) -f native.mk desktop\nnative-image:\n\t$(MAKE) -f native.mk image\nnative-check:\n\t$(MAKE) -f native.mk check\nnative-clean:\n\t$(MAKE) -f native.mk clean\nclean: native-clean\nnative-x86-iso:\n\t$(MAKE) -f native.mk x86-iso\n'
        pending['Makefile']=original
        relative=str(makefile.relative_to(ROOT))
        if relative in LEGACY_HASHES:UPDATED_LEGACY[relative]=hashlib.sha256(original).hexdigest()
    pending['native-names.tsv']=('original\tlocalized\tstatus\n'+''.join(old+'\t'+new+'\tfunctional-proposal\n' for old,new in sorted(mapping.items()))).encode()
    pending['native-term-evidence.json']=(json.dumps({'policy':'Whole-role functional proposals. Do not attribute a single philosophy to an entire country. Unreviewed etymologies are not asserted.',
        'sources':['WorldOS naming/terms.json (CLDR language selection and prior proposals)','golang/worldos/tools/naming_lexicon.py (whole-role paths)','WorldOS native/terms.py (current implementation roles)'],
        'review':'Native-speaker review pending; proposals are not official standard terminology.',
        'lexical_evidence':json.loads((ROOT/'native/inputs/term-evidence.json').read_text()).get(language,[]),
        'thread_example':{'name':mapping.get('작업가닥','작업가닥'),'meaning':'An independently scheduled execution sequence; current kernel schedules cooperatively.',
            'historical_root': 'German Faden: documented Middle/Old High German forms; the compound Arbeitsfaden is a project proposal, not an ancient computing term.' if language=='de' else 'No language-specific historical claim.',
            'reference':'https://www.duden.de/rechtschreibung/Faden' if language=='de' else None}},ensure_ascii=False,indent=2)+'\n').encode()
    snapshot = ROOT / 'native/inputs/localized-roles' / (language + '.json')
    if snapshot.is_file():
        proposals = json.loads(snapshot.read_text())
        evidence = json.loads(pending['native-term-evidence.json'].decode())
        evidence['terminology_proposals'] = {key: proposals.get(key) for key in (
            'references', 'archive_sha256', 'archive_member', 'scope', 'status',
            'native_review', 'etymology_review')}
        evidence['terminology_proposals']['whole_roles'] = len(proposals.get('roles', {}))
        evidence['terminology_proposals']['pending_roles'] = len(proposals.get('pending_roles', {}))
        pending['native-term-evidence.json'] = (json.dumps(evidence, ensure_ascii=False, indent=2) + '\n').encode()
    pending['native-pending.tsv']=('identifier\tstatus\n'+''.join(word+'\ttranslation-review-required\n' for word in sorted(untranslated) if language!='ko')).encode()
    pending['NATIVE.md']=('\n'.join(['# '+code+' — '+native_name,'',help_text,'',
        '```sh',*(['make native-build','make native-desktop ARGS=--network','make native-run','make native-image'] if edition else ['make build','make desktop ARGS=--network','make run','make image']),'```','',
        'Source: `'+source_name+'`; examples: `'+('native-example' if edition else 'example')+'/`.','Guest: `help input`, `example java`, `cd /example/java`, `vi '+config['examples']['출력예제']+'.java`.',
        'Build: Python 3, JDK javac (--release 8), Clang/Clang++, aarch64-linux-gnu binutils, libnewlib-dev.',
        'Bundled QEMU: x86_64 Linux. Other hosts: set QEMU_AARCH64 to a raspi4b-capable QEMU.',
        'No build-time dependency on another country, /home/user/jkoros, or golang/worldos.',
        'Country archives: independent regular native-vendor.tar.gz and qemu-host.tar.gz; language subfolders use the parent country archives. Copy the entire country for offline independence.',
        'The country folder can be copied and built without the WorldOS shared resources.',
        'To export only the generated native sources, use make native-export COUNTRY='+code+' OUTPUT=/path/to/new-directory.',
        'Existing Linux editions under language-code folders are preserved. Their Makefiles add native-* targets; make -f native.mk x86-iso builds the copied x86 kernel.',
        'Names: native-names.tsv; incomplete translations: native-pending.tsv. Native-speaker and historical-etymology review remains pending.',
        'Rendering: BMP glyphs + emoji; complex-script shaping and full bidirectional layout remain incomplete.',
        'Input: '+inputs[language]['kind']+'; '+inputs[language].get('limitations','US host positions; AltGr for additional symbols.'),
        '', 'Network / system: `help system` (standard and local command names both accepted).',
        'IP configuration: edit project `ip.conf`; default `192.168.0.100/24`, gateway `192.168.0.1`. An `ip.conf` beside `native.json` overrides the shared file. Standalone copies use `'+source_name+'/ip.conf`. Rebuild/restart after changes; regenerate board images too.',
        'IPv4: `ipconfig`, `ipconfig set 192.168.0.120 255.255.255.0 192.168.0.1`, `ip addr show`, `ping -c 4 192.168.0.1`.',
        'Status: `route`, `netstat` / `ss`, `ps`, `top` (q quits), `free`, `df`, `uptime`; shutdown: `poweroff`.',
        'Settings last until reboot. df measures RAM files, not SD. ps measures native tasks, not Linux processes.',
        'Inbound NAT after changing IP: `make desktop ARGS="--network --guest-ip 192.168.0.120"`, then configure that IP in the guest.',
        'Independent concurrent VM network: add `--network-host 127.0.0.2 --port 5903`.',
        '', '| Standard | Local command |', '|---|---|',
        *['| `'+key+'` | `'+config['commands']['aliases'][key]+'` |' for key in COMMAND_KEYS],
        '', 'Command translations still pending: '+(', '.join(config['commands']['pending']) or 'none')+'.',
        'Command names are functional proposals; native-speaker terminology review remains pending.',
        'The native kernel retains its existing JVM/Python/C/network limits. No full Java SE, SD filesystem, physical Pi input/network driver claim.'])+'\n').encode()
    stamp=folder/'native-generated.json';previous=json.loads(stamp.read_text()) if stamp.exists() else {}
    if any(name.endswith('.java') and data.startswith(COPYRIGHT) for name,data in base.items()):
        for name,data in list(pending.items()):
            if name.endswith('.java') and not data.startswith(COPYRIGHT):pending[name]=COPYRIGHT+data
    for name,data in pending.items():
        path=folder/name
        expected=previous.get(name)
        if name=='Makefile' and edition is not None and expected is None:expected=LEGACY_HASHES.get(str(path.relative_to(ROOT)))
        if path.is_file() and path.read_bytes()!=data and not matches_owned(path.read_bytes(),expected):
            raise SystemExit('Refusing to overwrite edited file: '+str(path))
    for name,data in pending.items():
        path=folder/name;path.parent.mkdir(parents=True,exist_ok=True)
        if not path.is_file() or path.read_bytes()!=data:path.write_bytes(data)
        if path.suffix=='.sh':path.chmod(0o755)
    for name,digest in previous.items():
        path=folder/name
        if name not in pending and path.is_file() and matches_owned(path.read_bytes(),digest):path.unlink()
    if edition is None:
        for name,archive in [('native-vendor.tar.gz',vendor),('qemu-host.tar.gz',host)]:
            copy_archive(folder/name,archive,archive_digest(archive))
    link=folder/('example' if edition is None else 'native-example')
    if not link.exists():link.symlink_to(source_name+'/example',target_is_directory=True)
    write_json(stamp,{name:hashlib.sha256(data).hexdigest() for name,data in pending.items()})
    return {k:config[k] for k in ('country','language','source','naming','input','examples')}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--countries',nargs='*');parser.add_argument('--vendor',action='store_true');parser.add_argument('--all-editions',action='store_true');parser.add_argument('--audit-only',action='store_true');args=parser.parse_args()
    if args.audit_only:
        paths=list((ROOT/'country').glob('*/native.json'))+list((ROOT/'country').glob('*/*/native.json'))
        pending=[]
        for path in paths:
            config=json.loads(path.read_text())
            if args.countries and config['country'] not in args.countries:continue
            files={'os/사용자/프로그램.mk':(JKOROS/'os/사용자/프로그램.mk').read_text().replace('사용자/자바/자바컴파일러.java','사용자/자바/자바컴파일러.java 사용자/자바/문자이름규칙.java')}
            if config['language']!='ko':files['도구/한글이름검사.sh']=(ROOT/'native/inputs/localized-audit.sh').read_text()
            manifest=path.parent/'native-generated.json';hashes=json.loads(manifest.read_text())
            for original,text in files.items():
                name=config['source']+'/'+translate(original,config['identifiers']);target=path.parent/name
                data=translate(text,config['identifiers']).encode()
                if target.read_bytes()==data:continue
                if hashlib.sha256(target.read_bytes()).hexdigest()!=hashes.get(name):raise SystemExit('Refusing to overwrite edited file: '+str(target))
                hashes[name]=hashlib.sha256(data).hexdigest();pending.append((target,data,manifest,hashes))
        for target,data,manifest,hashes in pending:target.write_bytes(data);target.chmod(0o755);write_json(manifest,hashes)
        print('Localized managed source audit:',len(pending));return
    OUTPUT.mkdir(parents=True,exist_ok=True)
    LEGACY_HASHES.update(json.loads((ROOT/'naming/generated-files.json').read_text()))
    rows=list(csv.DictReader((ROOT/'native/inputs/representatives.tsv').open(),delimiter='\t'))
    if args.countries:rows=[row for row in rows if row['country_alpha3'] in args.countries]
    base=sources();vendor=vendor_bundle() if args.vendor or not (OUTPUT/'native-vendor.tar.gz').exists() else OUTPUT/'native-vendor.tar.gz'
    vendor=publish_archive(vendor)
    host=publish_archive(OUTPUT/'qemu-host.tar.gz')
    inputs={language:profile(language) for language in sorted({row['language'] for row in rows})}
    report=[]
    for row in rows:
        report.append(generate(row,base,vendor,host,inputs));print(row['country_alpha3'],row['language'],flush=True)
    language_editions=[]
    if args.all_editions:
        for edition in json.loads((ROOT/'editions.json').read_text()):
            if args.countries and edition['country'] not in args.countries:continue
            language=edition['language']
            if language not in inputs:inputs[language]=profile(language)
            row={'country_alpha3':edition['country'],'language':language,'native_name':language}
            language_editions.append(generate(row,base,vendor,host,inputs,edition))
            print(edition['path'],flush=True)
        write_json(ROOT/'build/native/language-editions.json',{'editions':len(language_editions),'languages':len({r['language'] for r in language_editions}),'results':language_editions,'native_review':'pending','etymology_review':'pending'})
    complete=[]
    for path in sorted((ROOT/'country').glob('*/native.json')):
        config=json.loads(path.read_text());complete.append({key:config[key] for key in ('country','language','source','naming','input','examples')})
    write_json(ROOT/'build/native/generated.json',{'countries':len(complete),'languages':len({r['language'] for r in complete}),'updated_countries':[r['country'] for r in report],'editions':complete,'physical_pi_tested':False})
    if UPDATED_LEGACY:
        LEGACY_HASHES.update(UPDATED_LEGACY);write_json(ROOT/'naming/generated-files.json',LEGACY_HASHES)
    current=json.loads((OUTPUT/'inputs.json').read_text()) if (OUTPUT/'inputs.json').exists() else {}
    current.update(inputs);write_json(OUTPUT/'inputs.json',current)


if __name__=='__main__':main()
