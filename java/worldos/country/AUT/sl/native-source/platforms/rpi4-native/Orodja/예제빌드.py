"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(koren_pot, shramba_pot, Izvedi_ukaz):
    원본자료=shramba_pot/'example';KR_podatki=koren_pot/'build/examples';KR_podatki.mkdir(parents=True,exist_ok=True)
    Razred_pot=KR_podatki/'classes';Razred_pot.mkdir(exist_ok=True)
    자바라이브러리만들기(koren_pot,Izvedi_ukaz)
    ip_settings = read_config(koren_pot)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KR_podatki/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Izvedi_ukaz(['javac','--release','8','-encoding','UTF-8','-cp',koren_pot/'build/java-library/classes','-d',Razred_pot]+자바실행)
    navodilo_SEQUENCE=['public final class 예제꾸러미 { public static int namesti_VALUE(int jezik) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    navodilo_SEQUENCE.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    꾸러미명세['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    navodilo_SEQUENCE.append('if(jezik==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for POT in [원본자료/'python/slovenščina.py'] + sorted((koren_pot/'PYTHON_most/knjižnica').glob('*.py')):
        vsebina_VALUE=guest_bytes(POT);tarča='/lib/'+POT.name
        if len(vsebina_VALUE)>16384: raise ValueError('Python library exceeds native VFS limit: '+tarča)
        navodilo_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(tarča,ensure_ascii=True),vsebina_VALUE.hex()))
        꾸러미명세[tarča]={'bytes':len(vsebina_VALUE),'sha256':hashlib.sha256(vsebina_VALUE).hexdigest()}
    navodilo_SEQUENCE.append('}')
    for LOOKUP_INDEX,jezik in enumerate(('java','c','python')):
        Datoteka_Seznam=[(podatki_položaj.name,podatki_položaj) for podatki_položaj in sorted((원본자료/jezik).iterdir()) if podatki_položaj.is_file()]
        if jezik=='java':Datoteka_Seznam += [(podatki_položaj.stem+'.class',Razred_pot/(podatki_položaj.stem+'.class')) for podatki_položaj in 자바실행]
        navodilo_SEQUENCE += ['if(jezik==%d){'%LOOKUP_INDEX,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%jezik]
        for Ime,POT in Datoteka_Seznam:
            vsebina_VALUE=guest_bytes(POT);tarča='/example/'+jezik+'/'+Ime
            if len(vsebina_VALUE)>16384 or len(tarča.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+tarča)
            navodilo_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(tarča,ensure_ascii=True),vsebina_VALUE.hex()))
            꾸러미명세[tarča]={'bytes':len(vsebina_VALUE),'sha256':hashlib.sha256(vsebina_VALUE).hexdigest()}
        navodilo_SEQUENCE += ['return 0;}']
    navodilo_SEQUENCE += ['return -22;}}']
    (koren_pot/'build/예제꾸러미.java').write_text('\n'.join(navodilo_SEQUENCE)+'\n')
    (KR_podatki/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
