"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, mee_nnyemiwu):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    klaàsị_ụzọ_ozi=결과자료/'classes';klaàsị_ụzọ_ozi.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,mee_nnyemiwu)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    mee_nnyemiwu(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',klaàsị_ụzọ_ozi]+자바실행)
    okwunkụzi_NSOTANSO=['public final class 예제꾸러미 { public static int wùbe_valuu(int Asụsụ) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    GỤ̀ỌM=guest_bytes(원본자료/'README.md')
    if len(GỤ̀ỌM)>16384: raise ValueError('example README exceeds native VFS limit')
    okwunkụzi_NSOTANSO.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%GỤ̀ỌM.hex())
    꾸러미명세['/example/README.md']={'bytes':len(GỤ̀ỌM),'sha256':hashlib.sha256(GỤ̀ỌM).hexdigest()}
    okwunkụzi_NSOTANSO.append('if(Asụsụ==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ụzọ_ozi in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/ọbaakwụkwọ').glob('*.py')):
        ndịnà_valuu=guest_bytes(ụzọ_ozi);ebenlereanya='/lib/'+ụzọ_ozi.name
        if len(ndịnà_valuu)>16384: raise ValueError('Python library exceeds native VFS limit: '+ebenlereanya)
        okwunkụzi_NSOTANSO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ebenlereanya,ensure_ascii=True),ndịnà_valuu.hex()))
        꾸러미명세[ebenlereanya]={'bytes':len(ndịnà_valuu),'sha256':hashlib.sha256(ndịnà_valuu).hexdigest()}
    okwunkụzi_NSOTANSO.append('}')
    for 색인,Asụsụ in enumerate(('java','c','python')):
        ọbọakwụkwọ_ndepụta=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Asụsụ).iterdir()) if 자료위치.is_file()]
        if Asụsụ=='java':ọbọakwụkwọ_ndepụta += [(자료위치.stem+'.class',klaàsị_ụzọ_ozi/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        okwunkụzi_NSOTANSO += ['if(Asụsụ==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Asụsụ]
        for Aha,ụzọ_ozi in ọbọakwụkwọ_ndepụta:
            ndịnà_valuu=guest_bytes(ụzọ_ozi);ebenlereanya='/example/'+Asụsụ+'/'+Aha
            if len(ndịnà_valuu)>16384 or len(ebenlereanya.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ebenlereanya)
            okwunkụzi_NSOTANSO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ebenlereanya,ensure_ascii=True),ndịnà_valuu.hex()))
            꾸러미명세[ebenlereanya]={'bytes':len(ndịnà_valuu),'sha256':hashlib.sha256(ndịnà_valuu).hexdigest()}
        okwunkụzi_NSOTANSO += ['return 0;}']
    okwunkụzi_NSOTANSO += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(okwunkụzi_NSOTANSO)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
