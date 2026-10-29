"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(erro_bide_izen, biltegi_bide_izen, exekutatu_komando):
    원본자료=biltegi_bide_izen/'example';neurria_datuak=erro_bide_izen/'build/examples';neurria_datuak.mkdir(parents=True,exist_ok=True)
    Gela_bide_izen=neurria_datuak/'classes';Gela_bide_izen.mkdir(exist_ok=True)
    자바라이브러리만들기(erro_bide_izen,exekutatu_komando)
    ip_settings = read_config(erro_bide_izen)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = neurria_datuak/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    exekutatu_komando(['javac','--release','8','-encoding','UTF-8','-cp',erro_bide_izen/'build/java-library/classes','-d',Gela_bide_izen]+자바실행)
    instrukzio_SEKUENTZIA=['public final class 예제꾸러미 { public static int instalatu_balio(int Hizkuntza) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    IRAKHAU=guest_bytes(원본자료/'README.md')
    if len(IRAKHAU)>16384: raise ValueError('example README exceeds native VFS limit')
    instrukzio_SEKUENTZIA.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%IRAKHAU.hex())
    꾸러미명세['/example/README.md']={'bytes':len(IRAKHAU),'sha256':hashlib.sha256(IRAKHAU).hexdigest()}
    instrukzio_SEKUENTZIA.append('if(Hizkuntza==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for Bide_izena in [원본자료/'python/Euskara.py'] + sorted((erro_bide_izen/'PYTHON_zubi/liburutegi').glob('*.py')):
        eduki_balio=guest_bytes(Bide_izena);helburu_balio='/lib/'+Bide_izena.name
        if len(eduki_balio)>16384: raise ValueError('Python library exceeds native VFS limit: '+helburu_balio)
        instrukzio_SEKUENTZIA.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(helburu_balio,ensure_ascii=True),eduki_balio.hex()))
        꾸러미명세[helburu_balio]={'bytes':len(eduki_balio),'sha256':hashlib.sha256(eduki_balio).hexdigest()}
    instrukzio_SEKUENTZIA.append('}')
    for BEGIRATU_INDIZE,Hizkuntza in enumerate(('java','c','python')):
        fitxategi_Zerrenda=[(datuak_kargu.name,datuak_kargu) for datuak_kargu in sorted((원본자료/Hizkuntza).iterdir()) if datuak_kargu.is_file()]
        if Hizkuntza=='java':fitxategi_Zerrenda += [(datuak_kargu.stem+'.class',Gela_bide_izen/(datuak_kargu.stem+'.class')) for datuak_kargu in 자바실행]
        instrukzio_SEKUENTZIA += ['if(Hizkuntza==%d){'%BEGIRATU_INDIZE,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Hizkuntza]
        for Izena,Bide_izena in fitxategi_Zerrenda:
            eduki_balio=guest_bytes(Bide_izena);helburu_balio='/example/'+Hizkuntza+'/'+Izena
            if len(eduki_balio)>16384 or len(helburu_balio.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+helburu_balio)
            instrukzio_SEKUENTZIA.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(helburu_balio,ensure_ascii=True),eduki_balio.hex()))
            꾸러미명세[helburu_balio]={'bytes':len(eduki_balio),'sha256':hashlib.sha256(eduki_balio).hexdigest()}
        instrukzio_SEKUENTZIA += ['return 0;}']
    instrukzio_SEKUENTZIA += ['return -22;}}']
    (erro_bide_izen/'build/예제꾸러미.java').write_text('\n'.join(instrukzio_SEKUENTZIA)+'\n')
    (neurria_datuak/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
