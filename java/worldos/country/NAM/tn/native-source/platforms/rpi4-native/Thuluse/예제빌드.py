"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, diragatsa_Taelo):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    mofuta_tsela=결과자료/'classes';mofuta_tsela.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,diragatsa_Taelo)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    diragatsa_Taelo(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',mofuta_tsela]+자바실행)
    taelo_TATELANO=['public final class 예제꾸러미 { public static int tsenya_Boleng(int Puo) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    MPUISE=guest_bytes(원본자료/'README.md')
    if len(MPUISE)>16384: raise ValueError('example README exceeds native VFS limit')
    taelo_TATELANO.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%MPUISE.hex())
    꾸러미명세['/example/README.md']={'bytes':len(MPUISE),'sha256':hashlib.sha256(MPUISE).hexdigest()}
    taelo_TATELANO.append('if(Puo==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for tsela in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/laeborari').glob('*.py')):
        Diteng_Boleng=guest_bytes(tsela);setotwa='/lib/'+tsela.name
        if len(Diteng_Boleng)>16384: raise ValueError('Python library exceeds native VFS limit: '+setotwa)
        taelo_TATELANO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(setotwa,ensure_ascii=True),Diteng_Boleng.hex()))
        꾸러미명세[setotwa]={'bytes':len(Diteng_Boleng),'sha256':hashlib.sha256(Diteng_Boleng).hexdigest()}
    taelo_TATELANO.append('}')
    for 색인,Puo in enumerate(('java','c','python')):
        faele_lenaane=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Puo).iterdir()) if 자료위치.is_file()]
        if Puo=='java':faele_lenaane += [(자료위치.stem+'.class',mofuta_tsela/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        taelo_TATELANO += ['if(Puo==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Puo]
        for leina,tsela in faele_lenaane:
            Diteng_Boleng=guest_bytes(tsela);setotwa='/example/'+Puo+'/'+leina
            if len(Diteng_Boleng)>16384 or len(setotwa.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+setotwa)
            taelo_TATELANO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(setotwa,ensure_ascii=True),Diteng_Boleng.hex()))
            꾸러미명세[setotwa]={'bytes':len(Diteng_Boleng),'sha256':hashlib.sha256(Diteng_Boleng).hexdigest()}
        taelo_TATELANO += ['return 0;}']
    taelo_TATELANO += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(taelo_TATELANO)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
