"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(gyök_útvonal, adattár_útvonal, végrehajt_parancs):
    원본자료=adattár_útvonal/'example';KR_adat=gyök_útvonal/'build/examples';KR_adat.mkdir(parents=True,exist_ok=True)
    tanóra_útvonal=KR_adat/'classes';tanóra_útvonal.mkdir(exist_ok=True)
    자바라이브러리만들기(gyök_útvonal,végrehajt_parancs)
    ip_settings = read_config(gyök_útvonal)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KR_adat/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    végrehajt_parancs(['javac','--release','8','-encoding','UTF-8','-cp',gyök_útvonal/'build/java-library/classes','-d',tanóra_útvonal]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int telepít_ÉRTÉK(int Nyelv) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    köteg_jegyzékfájl={}
    fontos_fájl=guest_bytes(원본자료/'README.md')
    if len(fontos_fájl)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%fontos_fájl.hex())
    köteg_jegyzékfájl['/example/README.md']={'bytes':len(fontos_fájl),'sha256':hashlib.sha256(fontos_fájl).hexdigest()}
    명령열.append('if(Nyelv==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ÚTVONAL in [원본자료/'python/magyar.py'] + sorted((gyök_útvonal/'PYTHON_híd/kódtár').glob('*.py')):
        Tartalom_ÉRTÉK=guest_bytes(ÚTVONAL);cél='/lib/'+ÚTVONAL.name
        if len(Tartalom_ÉRTÉK)>16384: raise ValueError('Python library exceeds native VFS limit: '+cél)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(cél,ensure_ascii=True),Tartalom_ÉRTÉK.hex()))
        köteg_jegyzékfájl[cél]={'bytes':len(Tartalom_ÉRTÉK),'sha256':hashlib.sha256(Tartalom_ÉRTÉK).hexdigest()}
    명령열.append('}')
    for KERES_INDEX,Nyelv in enumerate(('java','c','python')):
        fájllista=[(adat_pozíció.name,adat_pozíció) for adat_pozíció in sorted((원본자료/Nyelv).iterdir()) if adat_pozíció.is_file()]
        if Nyelv=='java':fájllista += [(adat_pozíció.stem+'.class',tanóra_útvonal/(adat_pozíció.stem+'.class')) for adat_pozíció in 자바실행]
        명령열 += ['if(Nyelv==%d){'%KERES_INDEX,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Nyelv]
        for Név,ÚTVONAL in fájllista:
            Tartalom_ÉRTÉK=guest_bytes(ÚTVONAL);cél='/example/'+Nyelv+'/'+Név
            if len(Tartalom_ÉRTÉK)>16384 or len(cél.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+cél)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(cél,ensure_ascii=True),Tartalom_ÉRTÉK.hex()))
            köteg_jegyzékfájl[cél]={'bytes':len(Tartalom_ÉRTÉK),'sha256':hashlib.sha256(Tartalom_ÉRTÉK).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (gyök_útvonal/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (KR_adat/'manifest.json').write_text(json.dumps(köteg_jegyzékfájl,ensure_ascii=False,indent=2)+'\n')
