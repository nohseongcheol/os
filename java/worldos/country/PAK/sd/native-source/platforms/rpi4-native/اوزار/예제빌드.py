"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, تعميل_ڪرڻ_حڪم):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    درجو_راههه=결과자료/'classes';درجو_راههه.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,تعميل_ڪرڻ_حڪم)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    تعميل_ڪرڻ_حڪم(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',درجو_راههه]+자바실행)
    هدايت_ترتيب=['public final class 예제꾸러미 { public static int نصب_ڪريو_قدر(int ٻولي) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    پڙهو_فائل=guest_bytes(원본자료/'README.md')
    if len(پڙهو_فائل)>16384: raise ValueError('example README exceeds native VFS limit')
    هدايت_ترتيب.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%پڙهو_فائل.hex())
    꾸러미명세['/example/README.md']={'bytes':len(پڙهو_فائل),'sha256':hashlib.sha256(پڙهو_فائل).hexdigest()}
    هدايت_ترتيب.append('if(ٻولي==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for راههه in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/لائبريري').glob('*.py')):
        مواد_قدر=guest_bytes(راههه);هدف='/lib/'+راههه.name
        if len(مواد_قدر)>16384: raise ValueError('Python library exceeds native VFS limit: '+هدف)
        هدايت_ترتيب.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(هدف,ensure_ascii=True),مواد_قدر.hex()))
        꾸러미명세[هدف]={'bytes':len(مواد_قدر),'sha256':hashlib.sha256(مواد_قدر).hexdigest()}
    هدايت_ترتيب.append('}')
    for 색인,ٻولي in enumerate(('java','c','python')):
        فائل_فهرست=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/ٻولي).iterdir()) if 자료위치.is_file()]
        if ٻولي=='java':فائل_فهرست += [(자료위치.stem+'.class',درجو_راههه/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        هدايت_ترتيب += ['if(ٻولي==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%ٻولي]
        for نالو,راههه in فائل_فهرست:
            مواد_قدر=guest_bytes(راههه);هدف='/example/'+ٻولي+'/'+نالو
            if len(مواد_قدر)>16384 or len(هدف.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+هدف)
            هدايت_ترتيب.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(هدف,ensure_ascii=True),مواد_قدر.hex()))
            꾸러미명세[هدف]={'bytes':len(مواد_قدر),'sha256':hashlib.sha256(مواد_قدر).hexdigest()}
        هدايت_ترتيب += ['return 0;}']
    هدايت_ترتيب += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(هدايت_ترتيب)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
