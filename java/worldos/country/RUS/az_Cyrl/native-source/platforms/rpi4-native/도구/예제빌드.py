"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, 실행):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    클래스경로=결과자료/'classes';클래스경로.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,실행)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    실행(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',클래스경로]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int 설치(int 언어) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    꾸러미명세['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    명령열.append('if(언어==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for 경로 in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/라이브러리').glob('*.py')):
        내용=guest_bytes(경로);대상='/lib/'+경로.name
        if len(내용)>16384 or len(대상.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+대상)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(대상,ensure_ascii=True),내용.hex()))
        꾸러미명세[대상]={'bytes':len(내용),'sha256':hashlib.sha256(내용).hexdigest()}
    명령열.append('}')
    for 색인,언어 in enumerate(('java','c','python')):
        파일목록=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/언어).iterdir()) if 자료위치.is_file()]
        if 언어=='java':파일목록 += [(자료위치.stem+'.class',클래스경로/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        명령열 += ['if(언어==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%언어]
        for 이름,경로 in 파일목록:
            내용=guest_bytes(경로);대상='/example/'+언어+'/'+이름
            if len(내용)>16384 or len(대상.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+대상)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(대상,ensure_ascii=True),내용.hex()))
            꾸러미명세[대상]={'bytes':len(내용),'sha256':hashlib.sha256(내용).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
