"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, matattara_Hanyar_shiga, gudanar_Umarni):
    원본자료=matattara_Hanyar_shiga/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    Aji_Hanyar_shiga=결과자료/'classes';Aji_Hanyar_shiga.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,gudanar_Umarni)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    gudanar_Umarni(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',Aji_Hanyar_shiga]+자바실행)
    Sharadi_JERI=['public final class 예제꾸러미 { public static int Girka_Daraja(int yare) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    README=guest_bytes(원본자료/'README.md')
    if len(README)>16384: raise ValueError('example README exceeds native VFS limit')
    Sharadi_JERI.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%README.hex())
    꾸러미명세['/example/README.md']={'bytes':len(README),'sha256':hashlib.sha256(README).hexdigest()}
    Sharadi_JERI.append('if(yare==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for Hanyar_shiga in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/laburare').glob('*.py')):
        kunshiya_Daraja=guest_bytes(Hanyar_shiga);tageti='/lib/'+Hanyar_shiga.name
        if len(kunshiya_Daraja)>16384: raise ValueError('Python library exceeds native VFS limit: '+tageti)
        Sharadi_JERI.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(tageti,ensure_ascii=True),kunshiya_Daraja.hex()))
        꾸러미명세[tageti]={'bytes':len(kunshiya_Daraja),'sha256':hashlib.sha256(kunshiya_Daraja).hexdigest()}
    Sharadi_JERI.append('}')
    for 색인,yare in enumerate(('java','c','python')):
        Fayil_Jeri=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/yare).iterdir()) if 자료위치.is_file()]
        if yare=='java':Fayil_Jeri += [(자료위치.stem+'.class',Aji_Hanyar_shiga/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        Sharadi_JERI += ['if(yare==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%yare]
        for Suna,Hanyar_shiga in Fayil_Jeri:
            kunshiya_Daraja=guest_bytes(Hanyar_shiga);tageti='/example/'+yare+'/'+Suna
            if len(kunshiya_Daraja)>16384 or len(tageti.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+tageti)
            Sharadi_JERI.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(tageti,ensure_ascii=True),kunshiya_Daraja.hex()))
            꾸러미명세[tageti]={'bytes':len(kunshiya_Daraja),'sha256':hashlib.sha256(kunshiya_Daraja).hexdigest()}
        Sharadi_JERI += ['return 0;}']
    Sharadi_JERI += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(Sharadi_JERI)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
