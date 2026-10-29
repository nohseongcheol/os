"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ=결과자료/'classes';ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ(int ᎦᏬᏂᎯᏍᏗ) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    ᏍᎩᎪᎵᏯ=guest_bytes(원본자료/'README.md')
    if len(ᏍᎩᎪᎵᏯ)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%ᏍᎩᎪᎵᏯ.hex())
    꾸러미명세['/example/README.md']={'bytes':len(ᏍᎩᎪᎵᏯ),'sha256':hashlib.sha256(ᏍᎩᎪᎵᏯ).hexdigest()}
    명령열.append('if(ᎦᏬᏂᎯᏍᏗ==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ᎠᏍᏓᏩᏛᏍᏗ in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/ᏧᏂᎪᎵᏰᏗᎢ').glob('*.py')):
        ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ=guest_bytes(ᎠᏍᏓᏩᏛᏍᏗ);ᎠᏉᏅᏗᎢ='/lib/'+ᎠᏍᏓᏩᏛᏍᏗ.name
        if len(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ)>16384 or len(ᎠᏉᏅᏗᎢ.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+ᎠᏉᏅᏗᎢ)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ᎠᏉᏅᏗᎢ,ensure_ascii=True),ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.hex()))
        꾸러미명세[ᎠᏉᏅᏗᎢ]={'bytes':len(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ),'sha256':hashlib.sha256(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ).hexdigest()}
    명령열.append('}')
    for 색인,ᎦᏬᏂᎯᏍᏗ in enumerate(('java','c','python')):
        ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/ᎦᏬᏂᎯᏍᏗ).iterdir()) if 자료위치.is_file()]
        if ᎦᏬᏂᎯᏍᏗ=='java':ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ += [(자료위치.stem+'.class',ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        명령열 += ['if(ᎦᏬᏂᎯᏍᏗ==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%ᎦᏬᏂᎯᏍᏗ]
        for ᏚᏙᎥᎢ,ᎠᏍᏓᏩᏛᏍᏗ in ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ:
            ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ=guest_bytes(ᎠᏍᏓᏩᏛᏍᏗ);ᎠᏉᏅᏗᎢ='/example/'+ᎦᏬᏂᎯᏍᏗ+'/'+ᏚᏙᎥᎢ
            if len(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ)>16384 or len(ᎠᏉᏅᏗᎢ.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ᎠᏉᏅᏗᎢ)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ᎠᏉᏅᏗᎢ,ensure_ascii=True),ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.hex()))
            꾸러미명세[ᎠᏉᏅᏗᎢ]={'bytes':len(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ),'sha256':hashlib.sha256(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
