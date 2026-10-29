"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(juuri_polku, säilö_polku, Suorita_komento):
    원본자료=säilö_polku/'example';KR_data=juuri_polku/'build/examples';KR_data.mkdir(parents=True,exist_ok=True)
    Luokka_polku=KR_data/'classes';Luokka_polku.mkdir(exist_ok=True)
    자바라이브러리만들기(juuri_polku,Suorita_komento)
    ip_settings = read_config(juuri_polku)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KR_data/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Suorita_komento(['javac','--release','8','-encoding','UTF-8','-cp',juuri_polku/'build/java-library/classes','-d',Luokka_polku]+자바실행)
    käsky_JONO=['public final class 예제꾸러미 { public static int asentaa_ARVO(int Kieli) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    nippu_kokoonpanotiedot={}
    Lueminut=guest_bytes(원본자료/'README.md')
    if len(Lueminut)>16384: raise ValueError('example README exceeds native VFS limit')
    käsky_JONO.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%Lueminut.hex())
    nippu_kokoonpanotiedot['/example/README.md']={'bytes':len(Lueminut),'sha256':hashlib.sha256(Lueminut).hexdigest()}
    käsky_JONO.append('if(Kieli==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for polku_2 in [원본자료/'python/suomi.py'] + sorted((juuri_polku/'PYTHON_silta/kirjasto').glob('*.py')):
        Sisältö_ARVO=guest_bytes(polku_2);tavoite='/lib/'+polku_2.name
        if len(Sisältö_ARVO)>16384: raise ValueError('Python library exceeds native VFS limit: '+tavoite)
        käsky_JONO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(tavoite,ensure_ascii=True),Sisältö_ARVO.hex()))
        nippu_kokoonpanotiedot[tavoite]={'bytes':len(Sisältö_ARVO),'sha256':hashlib.sha256(Sisältö_ARVO).hexdigest()}
    käsky_JONO.append('}')
    for HAKU_INDEKSI,Kieli in enumerate(('java','c','python')):
        tiedostoluettelo=[(data_toimi.name,data_toimi) for data_toimi in sorted((원본자료/Kieli).iterdir()) if data_toimi.is_file()]
        if Kieli=='java':tiedostoluettelo += [(data_toimi.stem+'.class',Luokka_polku/(data_toimi.stem+'.class')) for data_toimi in 자바실행]
        käsky_JONO += ['if(Kieli==%d){'%HAKU_INDEKSI,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Kieli]
        for Nimi,polku_2 in tiedostoluettelo:
            Sisältö_ARVO=guest_bytes(polku_2);tavoite='/example/'+Kieli+'/'+Nimi
            if len(Sisältö_ARVO)>16384 or len(tavoite.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+tavoite)
            käsky_JONO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(tavoite,ensure_ascii=True),Sisältö_ARVO.hex()))
            nippu_kokoonpanotiedot[tavoite]={'bytes':len(Sisältö_ARVO),'sha256':hashlib.sha256(Sisältö_ARVO).hexdigest()}
        käsky_JONO += ['return 0;}']
    käsky_JONO += ['return -22;}}']
    (juuri_polku/'build/예제꾸러미.java').write_text('\n'.join(käsky_JONO)+'\n')
    (KR_data/'manifest.json').write_text(json.dumps(nippu_kokoonpanotiedot,ensure_ascii=False,indent=2)+'\n')
