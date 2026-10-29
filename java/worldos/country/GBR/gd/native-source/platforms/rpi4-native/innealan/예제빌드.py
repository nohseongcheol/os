"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(freumh_slighe, 저장소경로, gnìomhaich_àithne):
    원본자료=저장소경로/'example';tomhas_dàta=freumh_slighe/'build/examples';tomhas_dàta.mkdir(parents=True,exist_ok=True)
    clas_slighe=tomhas_dàta/'classes';clas_slighe.mkdir(exist_ok=True)
    자바라이브러리만들기(freumh_slighe,gnìomhaich_àithne)
    ip_settings = read_config(freumh_slighe)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = tomhas_dàta/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    gnìomhaich_àithne(['javac','--release','8','-encoding','UTF-8','-cp',freumh_slighe/'build/java-library/classes','-d',clas_slighe]+자바실행)
    treòrachadh_SEQUENCE=['public final class 예제꾸러미 { public static int stàlaich_VALUE(int cànan) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    LEUGHMI=guest_bytes(원본자료/'README.md')
    if len(LEUGHMI)>16384: raise ValueError('example README exceeds native VFS limit')
    treòrachadh_SEQUENCE.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%LEUGHMI.hex())
    꾸러미명세['/example/README.md']={'bytes':len(LEUGHMI),'sha256':hashlib.sha256(LEUGHMI).hexdigest()}
    treòrachadh_SEQUENCE.append('if(cànan==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for Slighe in [원본자료/'python/한국어.py'] + sorted((freumh_slighe/'PYTHON_drochaid/leabhar_lann').glob('*.py')):
        susbaint_VALUE=guest_bytes(Slighe);targaid='/lib/'+Slighe.name
        if len(susbaint_VALUE)>16384: raise ValueError('Python library exceeds native VFS limit: '+targaid)
        treòrachadh_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(targaid,ensure_ascii=True),susbaint_VALUE.hex()))
        꾸러미명세[targaid]={'bytes':len(susbaint_VALUE),'sha256':hashlib.sha256(susbaint_VALUE).hexdigest()}
    treòrachadh_SEQUENCE.append('}')
    for LOOKUP_INDEX,cànan in enumerate(('java','c','python')):
        faidhle_Liosta=[(dàta_suidhich.name,dàta_suidhich) for dàta_suidhich in sorted((원본자료/cànan).iterdir()) if dàta_suidhich.is_file()]
        if cànan=='java':faidhle_Liosta += [(dàta_suidhich.stem+'.class',clas_slighe/(dàta_suidhich.stem+'.class')) for dàta_suidhich in 자바실행]
        treòrachadh_SEQUENCE += ['if(cànan==%d){'%LOOKUP_INDEX,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%cànan]
        for Ainm,Slighe in faidhle_Liosta:
            susbaint_VALUE=guest_bytes(Slighe);targaid='/example/'+cànan+'/'+Ainm
            if len(susbaint_VALUE)>16384 or len(targaid.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+targaid)
            treòrachadh_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(targaid,ensure_ascii=True),susbaint_VALUE.hex()))
            꾸러미명세[targaid]={'bytes':len(susbaint_VALUE),'sha256':hashlib.sha256(susbaint_VALUE).hexdigest()}
        treòrachadh_SEQUENCE += ['return 0;}']
    treòrachadh_SEQUENCE += ['return -22;}}']
    (freumh_slighe/'build/예제꾸러미.java').write_text('\n'.join(treòrachadh_SEQUENCE)+'\n')
    (tomhas_dàta/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
