"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, gukora_ibwiriza):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    icyiciro_inzira=결과자료/'classes';icyiciro_inzira.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,gukora_ibwiriza)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    gukora_ibwiriza(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',icyiciro_inzira]+자바실행)
    ibwiriza_URUKURIKIRANE=['public final class 예제꾸러미 { public static int kwinjiza_agaciro(int Ururimi) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    NSOMA=guest_bytes(원본자료/'README.md')
    if len(NSOMA)>16384: raise ValueError('example README exceeds native VFS limit')
    ibwiriza_URUKURIKIRANE.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%NSOMA.hex())
    꾸러미명세['/example/README.md']={'bytes':len(NSOMA),'sha256':hashlib.sha256(NSOMA).hexdigest()}
    ibwiriza_URUKURIKIRANE.append('if(Ururimi==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for Inzira in [원본자료/'python/Ikinyarwanda.py'] + sorted((기준경로/'파이썬연결/isomero').glob('*.py')):
        Ibirimo_agaciro=guest_bytes(Inzira);gusimbuza_igishya='/lib/'+Inzira.name
        if len(Ibirimo_agaciro)>16384: raise ValueError('Python library exceeds native VFS limit: '+gusimbuza_igishya)
        ibwiriza_URUKURIKIRANE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(gusimbuza_igishya,ensure_ascii=True),Ibirimo_agaciro.hex()))
        꾸러미명세[gusimbuza_igishya]={'bytes':len(Ibirimo_agaciro),'sha256':hashlib.sha256(Ibirimo_agaciro).hexdigest()}
    ibwiriza_URUKURIKIRANE.append('}')
    for 색인,Ururimi in enumerate(('java','c','python')):
        dosiye_Urutonde=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Ururimi).iterdir()) if 자료위치.is_file()]
        if Ururimi=='java':dosiye_Urutonde += [(자료위치.stem+'.class',icyiciro_inzira/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        ibwiriza_URUKURIKIRANE += ['if(Ururimi==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Ururimi]
        for Izina,Inzira in dosiye_Urutonde:
            Ibirimo_agaciro=guest_bytes(Inzira);gusimbuza_igishya='/example/'+Ururimi+'/'+Izina
            if len(Ibirimo_agaciro)>16384 or len(gusimbuza_igishya.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+gusimbuza_igishya)
            ibwiriza_URUKURIKIRANE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(gusimbuza_igishya,ensure_ascii=True),Ibirimo_agaciro.hex()))
            꾸러미명세[gusimbuza_igishya]={'bytes':len(Ibirimo_agaciro),'sha256':hashlib.sha256(Ibirimo_agaciro).hexdigest()}
        ibwiriza_URUKURIKIRANE += ['return 0;}']
    ibwiriza_URUKURIKIRANE += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(ibwiriza_URUKURIKIRANE)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
