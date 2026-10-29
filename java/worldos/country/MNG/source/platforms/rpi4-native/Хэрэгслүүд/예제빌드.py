"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, Гүйцэтгэх_команд):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    класс_зам=결과자료/'classes';класс_зам.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,Гүйцэтгэх_команд)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Гүйцэтгэх_команд(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',класс_зам]+자바실행)
    заавар_ДАРААЛАЛ=['public final class 예제꾸러미 { public static int суулгах_утга(int Хэл) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    заавал_унших=guest_bytes(원본자료/'README.md')
    if len(заавал_унших)>16384: raise ValueError('example README exceeds native VFS limit')
    заавар_ДАРААЛАЛ.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%заавал_унших.hex())
    꾸러미명세['/example/README.md']={'bytes':len(заавал_унших),'sha256':hashlib.sha256(заавал_унших).hexdigest()}
    заавар_ДАРААЛАЛ.append('if(Хэл==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ЗАМ in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/сан').glob('*.py')):
        Агуулга_утга=guest_bytes(ЗАМ);зорилго='/lib/'+ЗАМ.name
        if len(Агуулга_утга)>16384: raise ValueError('Python library exceeds native VFS limit: '+зорилго)
        заавар_ДАРААЛАЛ.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(зорилго,ensure_ascii=True),Агуулга_утга.hex()))
        꾸러미명세[зорилго]={'bytes':len(Агуулга_утга),'sha256':hashlib.sha256(Агуулга_утга).hexdigest()}
    заавар_ДАРААЛАЛ.append('}')
    for 색인,Хэл in enumerate(('java','c','python')):
        файл_Жагсаалт=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Хэл).iterdir()) if 자료위치.is_file()]
        if Хэл=='java':файл_Жагсаалт += [(자료위치.stem+'.class',класс_зам/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        заавар_ДАРААЛАЛ += ['if(Хэл==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Хэл]
        for Нэр,ЗАМ in файл_Жагсаалт:
            Агуулга_утга=guest_bytes(ЗАМ);зорилго='/example/'+Хэл+'/'+Нэр
            if len(Агуулга_утга)>16384 or len(зорилго.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+зорилго)
            заавар_ДАРААЛАЛ.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(зорилго,ensure_ascii=True),Агуулга_утга.hex()))
            꾸러미명세[зорилго]={'bytes':len(Агуулга_утга),'sha256':hashlib.sha256(Агуулга_утга).hexdigest()}
        заавар_ДАРААЛАЛ += ['return 0;}']
    заавар_ДАРААЛАЛ += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(заавар_ДАРААЛАЛ)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
