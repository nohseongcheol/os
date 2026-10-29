"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(kořen_cesta, úložiště_cesta, Provést_příkaz):
    원본자료=úložiště_cesta/'example';KV_data=kořen_cesta/'build/examples';KV_data.mkdir(parents=True,exist_ok=True)
    Třída_cesta=KV_data/'classes';Třída_cesta.mkdir(exist_ok=True)
    자바라이브러리만들기(kořen_cesta,Provést_příkaz)
    ip_settings = read_config(kořen_cesta)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KV_data/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Provést_příkaz(['javac','--release','8','-encoding','UTF-8','-cp',kořen_cesta/'build/java-library/classes','-d',Třída_cesta]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int instalovat_HODNOTA(int Jazyk) { int 처리값;',
          '처리값=příkaz_interpret.예제폴더("/example"); if(처리값<0)return 처리값;']
    sada_manifest={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=příkaz_interpret.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    sada_manifest['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    명령열.append('if(Jazyk==0){처리값=příkaz_interpret.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for cesta_2 in [원본자료/'python/čeština.py'] + sorted((kořen_cesta/'PYTHON_most/knihovna').glob('*.py')):
        Obsah_HODNOTA=guest_bytes(cesta_2);cílová_úroveň='/lib/'+cesta_2.name
        if len(Obsah_HODNOTA)>16384 or len(cílová_úroveň.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+cílová_úroveň)
        명령열.append('처리값=příkaz_interpret.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(cílová_úroveň,ensure_ascii=True),Obsah_HODNOTA.hex()))
        sada_manifest[cílová_úroveň]={'bytes':len(Obsah_HODNOTA),'sha256':hashlib.sha256(Obsah_HODNOTA).hexdigest()}
    명령열.append('}')
    for VYHLEDAT_INDEX,Jazyk in enumerate(('java','c','python')):
        seznam_souborů=[(data_pozice.name,data_pozice) for data_pozice in sorted((원본자료/Jazyk).iterdir()) if data_pozice.is_file()]
        if Jazyk=='java':seznam_souborů += [(data_pozice.stem+'.class',Třída_cesta/(data_pozice.stem+'.class')) for data_pozice in 자바실행]
        명령열 += ['if(Jazyk==%d){'%VYHLEDAT_INDEX,'처리값=příkaz_interpret.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Jazyk]
        for Název,cesta_2 in seznam_souborů:
            Obsah_HODNOTA=guest_bytes(cesta_2);cílová_úroveň='/example/'+Jazyk+'/'+Název
            if len(Obsah_HODNOTA)>16384 or len(cílová_úroveň.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+cílová_úroveň)
            명령열.append('처리값=příkaz_interpret.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(cílová_úroveň,ensure_ascii=True),Obsah_HODNOTA.hex()))
            sada_manifest[cílová_úroveň]={'bytes':len(Obsah_HODNOTA),'sha256':hashlib.sha256(Obsah_HODNOTA).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (kořen_cesta/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (KV_data/'manifest.json').write_text(json.dumps(sada_manifest,ensure_ascii=False,indent=2)+'\n')
