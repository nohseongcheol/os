"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(koren_putanja, depo_putanja, Izvrši_komanda):
    원본자료=depo_putanja/'example';KR_podaci=koren_putanja/'build/examples';KR_podaci.mkdir(parents=True,exist_ok=True)
    Razred_putanja=KR_podaci/'classes';Razred_putanja.mkdir(exist_ok=True)
    자바라이브러리만들기(koren_putanja,Izvrši_komanda)
    ip_settings = read_config(koren_putanja)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KR_podaci/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Izvrši_komanda(['javac','--release','8','-encoding','UTF-8','-cp',koren_putanja/'build/java-library/classes','-d',Razred_putanja]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int instaliraj_VALUE(int jezik) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    꾸러미명세['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    명령열.append('if(jezik==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for putanja in [원본자료/'python/한국어.py'] + sorted((koren_putanja/'PYTHON_most/biblioteka').glob('*.py')):
        Sadržaj_VALUE=guest_bytes(putanja);cilj='/lib/'+putanja.name
        if len(Sadržaj_VALUE)>16384: raise ValueError('Python library exceeds native VFS limit: '+cilj)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(cilj,ensure_ascii=True),Sadržaj_VALUE.hex()))
        꾸러미명세[cilj]={'bytes':len(Sadržaj_VALUE),'sha256':hashlib.sha256(Sadržaj_VALUE).hexdigest()}
    명령열.append('}')
    for LOOKUP_INDEX,jezik in enumerate(('java','c','python')):
        Datoteka_Lista=[(podaci_pozicija.name,podaci_pozicija) for podaci_pozicija in sorted((원본자료/jezik).iterdir()) if podaci_pozicija.is_file()]
        if jezik=='java':Datoteka_Lista += [(podaci_pozicija.stem+'.class',Razred_putanja/(podaci_pozicija.stem+'.class')) for podaci_pozicija in 자바실행]
        명령열 += ['if(jezik==%d){'%LOOKUP_INDEX,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%jezik]
        for ime,putanja in Datoteka_Lista:
            Sadržaj_VALUE=guest_bytes(putanja);cilj='/example/'+jezik+'/'+ime
            if len(Sadržaj_VALUE)>16384 or len(cilj.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+cilj)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(cilj,ensure_ascii=True),Sadržaj_VALUE.hex()))
            꾸러미명세[cilj]={'bytes':len(Sadržaj_VALUE),'sha256':hashlib.sha256(Sadržaj_VALUE).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (koren_putanja/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (KR_podaci/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
