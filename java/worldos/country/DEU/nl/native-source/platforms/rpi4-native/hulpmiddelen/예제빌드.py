"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(wortel_pad, opslagplaats_pad, Uitvoeren_opdracht):
    원본자료=opslagplaats_pad/'example';HR_gegevens=wortel_pad/'build/examples';HR_gegevens.mkdir(parents=True,exist_ok=True)
    les_pad=HR_gegevens/'classes';les_pad.mkdir(exist_ok=True)
    자바라이브러리만들기(wortel_pad,Uitvoeren_opdracht)
    ip_settings = read_config(wortel_pad)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = HR_gegevens/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Uitvoeren_opdracht(['javac','--release','8','-encoding','UTF-8','-cp',wortel_pad/'build/java-library/classes','-d',les_pad]+자바실행)
    instructie_REEKS=['public final class 예제꾸러미 { public static int installeren_WAARDE(int Taal) { int 처리값;',
          '처리값=Opdrachtvertolker.예제폴더("/example"); if(처리값<0)return 처리값;']
    bundel_manifest={}
    LEESMIJ=guest_bytes(원본자료/'README.md')
    if len(LEESMIJ)>16384: raise ValueError('example README exceeds native VFS limit')
    instructie_REEKS.append('처리값=Opdrachtvertolker.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%LEESMIJ.hex())
    bundel_manifest['/example/README.md']={'bytes':len(LEESMIJ),'sha256':hashlib.sha256(LEESMIJ).hexdigest()}
    instructie_REEKS.append('if(Taal==0){처리값=Opdrachtvertolker.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for pad in [원본자료/'python/Nederlands.py'] + sorted((wortel_pad/'PYTHON_brug/bibliotheek').glob('*.py')):
        Inhoud_WAARDE=guest_bytes(pad);doel='/lib/'+pad.name
        if len(Inhoud_WAARDE)>16384: raise ValueError('Python library exceeds native VFS limit: '+doel)
        instructie_REEKS.append('처리값=Opdrachtvertolker.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(doel,ensure_ascii=True),Inhoud_WAARDE.hex()))
        bundel_manifest[doel]={'bytes':len(Inhoud_WAARDE),'sha256':hashlib.sha256(Inhoud_WAARDE).hexdigest()}
    instructie_REEKS.append('}')
    for ZOEKEN_INDEX,Taal in enumerate(('java','c','python')):
        bestandslijst=[(gegevens_functie.name,gegevens_functie) for gegevens_functie in sorted((원본자료/Taal).iterdir()) if gegevens_functie.is_file()]
        if Taal=='java':bestandslijst += [(gegevens_functie.stem+'.class',les_pad/(gegevens_functie.stem+'.class')) for gegevens_functie in 자바실행]
        instructie_REEKS += ['if(Taal==%d){'%ZOEKEN_INDEX,'처리값=Opdrachtvertolker.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Taal]
        for Naam,pad in bestandslijst:
            Inhoud_WAARDE=guest_bytes(pad);doel='/example/'+Taal+'/'+Naam
            if len(Inhoud_WAARDE)>16384 or len(doel.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+doel)
            instructie_REEKS.append('처리값=Opdrachtvertolker.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(doel,ensure_ascii=True),Inhoud_WAARDE.hex()))
            bundel_manifest[doel]={'bytes':len(Inhoud_WAARDE),'sha256':hashlib.sha256(Inhoud_WAARDE).hexdigest()}
        instructie_REEKS += ['return 0;}']
    instructie_REEKS += ['return -22;}}']
    (wortel_pad/'build/예제꾸러미.java').write_text('\n'.join(instructie_REEKS)+'\n')
    (HR_gegevens/'manifest.json').write_text(json.dumps(bundel_manifest,ensure_ascii=False,indent=2)+'\n')
