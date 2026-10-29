"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(juur_tee, hoidla_tee, Täida_käsk):
    원본자료=hoidla_tee/'example';näitaja_andmed=juur_tee/'build/examples';näitaja_andmed.mkdir(parents=True,exist_ok=True)
    tund_tee=näitaja_andmed/'classes';tund_tee.mkdir(exist_ok=True)
    자바라이브러리만들기(juur_tee,Täida_käsk)
    ip_settings = read_config(juur_tee)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = näitaja_andmed/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Täida_käsk(['javac','--release','8','-encoding','UTF-8','-cp',juur_tee/'build/java-library/classes','-d',tund_tee]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int installima_VALUE(int Keeled) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    꾸러미명세['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    명령열.append('if(Keeled==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for RADA in [원본자료/'python/Eesti.py'] + sorted((juur_tee/'PYTHON_sild/teek').glob('*.py')):
        Sisu_VALUE=guest_bytes(RADA);siht='/lib/'+RADA.name
        if len(Sisu_VALUE)>16384: raise ValueError('Python library exceeds native VFS limit: '+siht)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(siht,ensure_ascii=True),Sisu_VALUE.hex()))
        꾸러미명세[siht]={'bytes':len(Sisu_VALUE),'sha256':hashlib.sha256(Sisu_VALUE).hexdigest()}
    명령열.append('}')
    for LOOKUP_INDEX,Keeled in enumerate(('java','c','python')):
        Fail_Loend=[(andmed_ametikoht.name,andmed_ametikoht) for andmed_ametikoht in sorted((원본자료/Keeled).iterdir()) if andmed_ametikoht.is_file()]
        if Keeled=='java':Fail_Loend += [(andmed_ametikoht.stem+'.class',tund_tee/(andmed_ametikoht.stem+'.class')) for andmed_ametikoht in 자바실행]
        명령열 += ['if(Keeled==%d){'%LOOKUP_INDEX,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Keeled]
        for Nimi_2,RADA in Fail_Loend:
            Sisu_VALUE=guest_bytes(RADA);siht='/example/'+Keeled+'/'+Nimi_2
            if len(Sisu_VALUE)>16384 or len(siht.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+siht)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(siht,ensure_ascii=True),Sisu_VALUE.hex()))
            꾸러미명세[siht]={'bytes':len(Sisu_VALUE),'sha256':hashlib.sha256(Sisu_VALUE).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (juur_tee/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (näitaja_andmed/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
