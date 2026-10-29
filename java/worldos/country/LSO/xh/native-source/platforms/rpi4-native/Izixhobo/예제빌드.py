"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, ukwenza_umyalelo):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    iklasi_indlela=결과자료/'classes';iklasi_indlela.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,ukwenza_umyalelo)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ukwenza_umyalelo(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',iklasi_indlela]+자바실행)
    umyalelo_ULANDELELWANO=['public final class 예제꾸러미 { public static int fakela_ixabiso(int Ulwimi) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    i_README=guest_bytes(원본자료/'README.md')
    if len(i_README)>16384: raise ValueError('example README exceeds native VFS limit')
    umyalelo_ULANDELELWANO.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%i_README.hex())
    꾸러미명세['/example/README.md']={'bytes':len(i_README),'sha256':hashlib.sha256(i_README).hexdigest()}
    umyalelo_ULANDELELWANO.append('if(Ulwimi==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for INDLELA in [원본자료/'python/isiXhosa.py'] + sorted((기준경로/'파이썬연결/ilayibhrari').glob('*.py')):
        Isiqulatho_ixabiso=guest_bytes(INDLELA);ithagethi='/lib/'+INDLELA.name
        if len(Isiqulatho_ixabiso)>16384: raise ValueError('Python library exceeds native VFS limit: '+ithagethi)
        umyalelo_ULANDELELWANO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ithagethi,ensure_ascii=True),Isiqulatho_ixabiso.hex()))
        꾸러미명세[ithagethi]={'bytes':len(Isiqulatho_ixabiso),'sha256':hashlib.sha256(Isiqulatho_ixabiso).hexdigest()}
    umyalelo_ULANDELELWANO.append('}')
    for 색인,Ulwimi in enumerate(('java','c','python')):
        ifayile_uludwe=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Ulwimi).iterdir()) if 자료위치.is_file()]
        if Ulwimi=='java':ifayile_uludwe += [(자료위치.stem+'.class',iklasi_indlela/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        umyalelo_ULANDELELWANO += ['if(Ulwimi==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Ulwimi]
        for Igama,INDLELA in ifayile_uludwe:
            Isiqulatho_ixabiso=guest_bytes(INDLELA);ithagethi='/example/'+Ulwimi+'/'+Igama
            if len(Isiqulatho_ixabiso)>16384 or len(ithagethi.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ithagethi)
            umyalelo_ULANDELELWANO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ithagethi,ensure_ascii=True),Isiqulatho_ixabiso.hex()))
            꾸러미명세[ithagethi]={'bytes':len(Isiqulatho_ixabiso),'sha256':hashlib.sha256(Isiqulatho_ixabiso).hexdigest()}
        umyalelo_ULANDELELWANO += ['return 0;}']
    umyalelo_ULANDELELWANO += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(umyalelo_ULANDELELWANO)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
