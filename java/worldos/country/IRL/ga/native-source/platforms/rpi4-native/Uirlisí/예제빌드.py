"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(fréamh_cosán, 저장소경로, Rith_ordú):
    원본자료=저장소경로/'example';tomhas_sonraí=fréamh_cosán/'build/examples';tomhas_sonraí.mkdir(parents=True,exist_ok=True)
    aicme_cosán=tomhas_sonraí/'classes';aicme_cosán.mkdir(exist_ok=True)
    자바라이브러리만들기(fréamh_cosán,Rith_ordú)
    ip_settings = read_config(fréamh_cosán)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = tomhas_sonraí/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Rith_ordú(['javac','--release','8','-encoding','UTF-8','-cp',fréamh_cosán/'build/java-library/classes','-d',aicme_cosán]+자바실행)
    treoir_SEQUENCE=['public final class 예제꾸러미 { public static int suiteáil_VALUE(int Teanga) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    LÉIGHMÉ=guest_bytes(원본자료/'README.md')
    if len(LÉIGHMÉ)>16384: raise ValueError('example README exceeds native VFS limit')
    treoir_SEQUENCE.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%LÉIGHMÉ.hex())
    꾸러미명세['/example/README.md']={'bytes':len(LÉIGHMÉ),'sha256':hashlib.sha256(LÉIGHMÉ).hexdigest()}
    treoir_SEQUENCE.append('if(Teanga==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for CONAIR in [원본자료/'python/Gaeilge.py'] + sorted((fréamh_cosán/'PYTHON_traschóiritheoir/leabharlann').glob('*.py')):
        Inneachar_VALUE=guest_bytes(CONAIR);sprioc='/lib/'+CONAIR.name
        if len(Inneachar_VALUE)>16384: raise ValueError('Python library exceeds native VFS limit: '+sprioc)
        treoir_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(sprioc,ensure_ascii=True),Inneachar_VALUE.hex()))
        꾸러미명세[sprioc]={'bytes':len(Inneachar_VALUE),'sha256':hashlib.sha256(Inneachar_VALUE).hexdigest()}
    treoir_SEQUENCE.append('}')
    for LOOKUP_INDEX,Teanga in enumerate(('java','c','python')):
        comhad_Liosta=[(sonraí_suíomh.name,sonraí_suíomh) for sonraí_suíomh in sorted((원본자료/Teanga).iterdir()) if sonraí_suíomh.is_file()]
        if Teanga=='java':comhad_Liosta += [(sonraí_suíomh.stem+'.class',aicme_cosán/(sonraí_suíomh.stem+'.class')) for sonraí_suíomh in 자바실행]
        treoir_SEQUENCE += ['if(Teanga==%d){'%LOOKUP_INDEX,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Teanga]
        for Ainm,CONAIR in comhad_Liosta:
            Inneachar_VALUE=guest_bytes(CONAIR);sprioc='/example/'+Teanga+'/'+Ainm
            if len(Inneachar_VALUE)>16384 or len(sprioc.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+sprioc)
            treoir_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(sprioc,ensure_ascii=True),Inneachar_VALUE.hex()))
            꾸러미명세[sprioc]={'bytes':len(Inneachar_VALUE),'sha256':hashlib.sha256(Inneachar_VALUE).hexdigest()}
        treoir_SEQUENCE += ['return 0;}']
    treoir_SEQUENCE += ['return -22;}}']
    (fréamh_cosán/'build/예제꾸러미.java').write_text('\n'.join(treoir_SEQUENCE)+'\n')
    (tomhas_sonraí/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
