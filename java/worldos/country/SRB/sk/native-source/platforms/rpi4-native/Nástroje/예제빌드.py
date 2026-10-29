"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(koreň_cesta, odkladací_priestor_cesta, Vykonať_príkaz):
    원본자료=odkladací_priestor_cesta/'example';KR_údaje=koreň_cesta/'build/examples';KR_údaje.mkdir(parents=True,exist_ok=True)
    lekcia_cesta=KR_údaje/'classes';lekcia_cesta.mkdir(exist_ok=True)
    자바라이브러리만들기(koreň_cesta,Vykonať_príkaz)
    ip_settings = read_config(koreň_cesta)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KR_údaje/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Vykonať_príkaz(['javac','--release','8','-encoding','UTF-8','-cp',koreň_cesta/'build/java-library/classes','-d',lekcia_cesta]+자바실행)
    inštrukcia_SEQUENCE=['public final class 예제꾸러미 { public static int inštalovať_VALUE(int Jazyky) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    zväzok_manifest_zostáv={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    inštrukcia_SEQUENCE.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    zväzok_manifest_zostáv['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    inštrukcia_SEQUENCE.append('if(Jazyky==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for Cesta in [원본자료/'python/Slovenský.py'] + sorted((koreň_cesta/'PYTHON_most/knižnica').glob('*.py')):
        obsah_VALUE=guest_bytes(Cesta);cieľová_hodnota='/lib/'+Cesta.name
        if len(obsah_VALUE)>16384: raise ValueError('Python library exceeds native VFS limit: '+cieľová_hodnota)
        inštrukcia_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(cieľová_hodnota,ensure_ascii=True),obsah_VALUE.hex()))
        zväzok_manifest_zostáv[cieľová_hodnota]={'bytes':len(obsah_VALUE),'sha256':hashlib.sha256(obsah_VALUE).hexdigest()}
    inštrukcia_SEQUENCE.append('}')
    for LOOKUP_INDEX,Jazyky in enumerate(('java','c','python')):
        Súbor_Zoznam=[(údaje_pozícia.name,údaje_pozícia) for údaje_pozícia in sorted((원본자료/Jazyky).iterdir()) if údaje_pozícia.is_file()]
        if Jazyky=='java':Súbor_Zoznam += [(údaje_pozícia.stem+'.class',lekcia_cesta/(údaje_pozícia.stem+'.class')) for údaje_pozícia in 자바실행]
        inštrukcia_SEQUENCE += ['if(Jazyky==%d){'%LOOKUP_INDEX,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Jazyky]
        for Názov,Cesta in Súbor_Zoznam:
            obsah_VALUE=guest_bytes(Cesta);cieľová_hodnota='/example/'+Jazyky+'/'+Názov
            if len(obsah_VALUE)>16384 or len(cieľová_hodnota.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+cieľová_hodnota)
            inštrukcia_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(cieľová_hodnota,ensure_ascii=True),obsah_VALUE.hex()))
            zväzok_manifest_zostáv[cieľová_hodnota]={'bytes':len(obsah_VALUE),'sha256':hashlib.sha256(obsah_VALUE).hexdigest()}
        inštrukcia_SEQUENCE += ['return 0;}']
    inštrukcia_SEQUENCE += ['return -22;}}']
    (koreň_cesta/'build/예제꾸러미.java').write_text('\n'.join(inštrukcia_SEQUENCE)+'\n')
    (KR_údaje/'manifest.json').write_text(json.dumps(zväzok_manifest_zostáv,ensure_ascii=False,indent=2)+'\n')
