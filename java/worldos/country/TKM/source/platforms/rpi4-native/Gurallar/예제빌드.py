"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, ýerine_ýetir_buýruk):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    klas_ýol=결과자료/'classes';klas_ýol.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,ýerine_ýetir_buýruk)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ýerine_ýetir_buýruk(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',klas_ýol]+자바실행)
    instruksiýa_SEQUENCE=['public final class 예제꾸러미 { public static int gurna_baha(int Dil) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    README=guest_bytes(원본자료/'README.md')
    if len(README)>16384: raise ValueError('example README exceeds native VFS limit')
    instruksiýa_SEQUENCE.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%README.hex())
    꾸러미명세['/example/README.md']={'bytes':len(README),'sha256':hashlib.sha256(README).hexdigest()}
    instruksiýa_SEQUENCE.append('if(Dil==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for Ýol in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/Kitaphana').glob('*.py')):
        Mazmun_baha=guest_bytes(Ýol);niýet='/lib/'+Ýol.name
        if len(Mazmun_baha)>16384: raise ValueError('Python library exceeds native VFS limit: '+niýet)
        instruksiýa_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(niýet,ensure_ascii=True),Mazmun_baha.hex()))
        꾸러미명세[niýet]={'bytes':len(Mazmun_baha),'sha256':hashlib.sha256(Mazmun_baha).hexdigest()}
    instruksiýa_SEQUENCE.append('}')
    for 색인,Dil in enumerate(('java','c','python')):
        faýl_Sanaw=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Dil).iterdir()) if 자료위치.is_file()]
        if Dil=='java':faýl_Sanaw += [(자료위치.stem+'.class',klas_ýol/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        instruksiýa_SEQUENCE += ['if(Dil==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Dil]
        for Ad,Ýol in faýl_Sanaw:
            Mazmun_baha=guest_bytes(Ýol);niýet='/example/'+Dil+'/'+Ad
            if len(Mazmun_baha)>16384 or len(niýet.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+niýet)
            instruksiýa_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(niýet,ensure_ascii=True),Mazmun_baha.hex()))
            꾸러미명세[niýet]={'bytes':len(Mazmun_baha),'sha256':hashlib.sha256(Mazmun_baha).hexdigest()}
        instruksiýa_SEQUENCE += ['return 0;}']
    instruksiýa_SEQUENCE += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(instruksiýa_SEQUENCE)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
