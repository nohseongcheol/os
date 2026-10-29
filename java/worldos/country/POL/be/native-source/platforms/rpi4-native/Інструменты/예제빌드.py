"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, рэпазіторый_шлях, выканаць_каманда):
    원본자료=рэпазіторый_шлях/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    клас_шлях=결과자료/'classes';клас_шлях.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,выканаць_каманда)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    выканаць_каманда(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',клас_шлях]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int усталяваць_значэнне(int Мова) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    файл_звестак=guest_bytes(원본자료/'README.md')
    if len(файл_звестак)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%файл_звестак.hex())
    꾸러미명세['/example/README.md']={'bytes':len(файл_звестак),'sha256':hashlib.sha256(файл_звестак).hexdigest()}
    명령열.append('if(Мова==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ШЛЯХ in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/бібліятэка').glob('*.py')):
        кантэнт_значэнне=guest_bytes(ШЛЯХ);мэтавы_паказчык='/lib/'+ШЛЯХ.name
        if len(кантэнт_значэнне)>16384 or len(мэтавы_паказчык.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+мэтавы_паказчык)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(мэтавы_паказчык,ensure_ascii=True),кантэнт_значэнне.hex()))
        꾸러미명세[мэтавы_паказчык]={'bytes':len(кантэнт_значэнне),'sha256':hashlib.sha256(кантэнт_значэнне).hexdigest()}
    명령열.append('}')
    for 색인,Мова in enumerate(('java','c','python')):
        файл_Спіс=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Мова).iterdir()) if 자료위치.is_file()]
        if Мова=='java':файл_Спіс += [(자료위치.stem+'.class',клас_шлях/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        명령열 += ['if(Мова==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Мова]
        for Назва,ШЛЯХ in файл_Спіс:
            кантэнт_значэнне=guest_bytes(ШЛЯХ);мэтавы_паказчык='/example/'+Мова+'/'+Назва
            if len(кантэнт_значэнне)>16384 or len(мэтавы_паказчык.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+мэтавы_паказчык)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(мэтавы_паказчык,ensure_ascii=True),кантэнт_значэнне.hex()))
            꾸러미명세[мэтавы_паказчык]={'bytes':len(кантэнт_значэнне),'sha256':hashlib.sha256(кантэнт_значэнне).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
