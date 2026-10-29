"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(radice_percorso, archivio_percorso, Esegui_comando):
    원본자료=archivio_percorso/'example';KR_dati=radice_percorso/'build/examples';KR_dati.mkdir(parents=True,exist_ok=True)
    Corso_percorso=KR_dati/'classes';Corso_percorso.mkdir(exist_ok=True)
    자바라이브러리만들기(radice_percorso,Esegui_comando)
    ip_settings = read_config(radice_percorso)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KR_dati/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Esegui_comando(['javac','--release','8','-encoding','UTF-8','-cp',radice_percorso/'build/java-library/classes','-d',Corso_percorso]+자바실행)
    istruzione_SEQUENZA=['public final class 예제꾸러미 { public static int installare_VALORE(int Lingua) { int 처리값;',
          '처리값=InterpreteComandi.예제폴더("/example"); if(처리값<0)return 처리값;']
    aggregare_manifesto={}
    README=guest_bytes(원본자료/'README.md')
    if len(README)>16384: raise ValueError('example README exceeds native VFS limit')
    istruzione_SEQUENZA.append('처리값=InterpreteComandi.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%README.hex())
    aggregare_manifesto['/example/README.md']={'bytes':len(README),'sha256':hashlib.sha256(README).hexdigest()}
    istruzione_SEQUENZA.append('if(Lingua==0){처리값=InterpreteComandi.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for percorso in [원본자료/'python/Italiano.py'] + sorted((radice_percorso/'PYTHON_bridge/Catalogo').glob('*.py')):
        Contenuto_VALORE=guest_bytes(percorso);target='/lib/'+percorso.name
        if len(Contenuto_VALORE)>16384: raise ValueError('Python library exceeds native VFS limit: '+target)
        istruzione_SEQUENZA.append('처리값=InterpreteComandi.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(target,ensure_ascii=True),Contenuto_VALORE.hex()))
        aggregare_manifesto[target]={'bytes':len(Contenuto_VALORE),'sha256':hashlib.sha256(Contenuto_VALORE).hexdigest()}
    istruzione_SEQUENZA.append('}')
    for CERCA_INDICE,Lingua in enumerate(('java','c','python')):
        elenco_file=[(dati_funzione.name,dati_funzione) for dati_funzione in sorted((원본자료/Lingua).iterdir()) if dati_funzione.is_file()]
        if Lingua=='java':elenco_file += [(dati_funzione.stem+'.class',Corso_percorso/(dati_funzione.stem+'.class')) for dati_funzione in 자바실행]
        istruzione_SEQUENZA += ['if(Lingua==%d){'%CERCA_INDICE,'처리값=InterpreteComandi.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Lingua]
        for Nome,percorso in elenco_file:
            Contenuto_VALORE=guest_bytes(percorso);target='/example/'+Lingua+'/'+Nome
            if len(Contenuto_VALORE)>16384 or len(target.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+target)
            istruzione_SEQUENZA.append('처리값=InterpreteComandi.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(target,ensure_ascii=True),Contenuto_VALORE.hex()))
            aggregare_manifesto[target]={'bytes':len(Contenuto_VALORE),'sha256':hashlib.sha256(Contenuto_VALORE).hexdigest()}
        istruzione_SEQUENZA += ['return 0;}']
    istruzione_SEQUENZA += ['return -22;}}']
    (radice_percorso/'build/예제꾸러미.java').write_text('\n'.join(istruzione_SEQUENZA)+'\n')
    (KR_dati/'manifest.json').write_text(json.dumps(aggregare_manifesto,ensure_ascii=False,indent=2)+'\n')
