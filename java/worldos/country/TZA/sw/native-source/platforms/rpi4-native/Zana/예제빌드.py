"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, uwekaji_njia, tekeleza_amri):
    원본자료=uwekaji_njia/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    tabaka_njia=결과자료/'classes';tabaka_njia.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,tekeleza_amri)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    tekeleza_amri(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',tabaka_njia]+자바실행)
    agizo_MFUATANO=['public final class 예제꾸러미 { public static int sakinisha_thamani(int Lugha) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    NISOME=guest_bytes(원본자료/'README.md')
    if len(NISOME)>16384: raise ValueError('example README exceeds native VFS limit')
    agizo_MFUATANO.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%NISOME.hex())
    꾸러미명세['/example/README.md']={'bytes':len(NISOME),'sha256':hashlib.sha256(NISOME).hexdigest()}
    agizo_MFUATANO.append('if(Lugha==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for njia in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/maktaba').glob('*.py')):
        maudhui_thamani=guest_bytes(njia);lengo='/lib/'+njia.name
        if len(maudhui_thamani)>16384: raise ValueError('Python library exceeds native VFS limit: '+lengo)
        agizo_MFUATANO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(lengo,ensure_ascii=True),maudhui_thamani.hex()))
        꾸러미명세[lengo]={'bytes':len(maudhui_thamani),'sha256':hashlib.sha256(maudhui_thamani).hexdigest()}
    agizo_MFUATANO.append('}')
    for 색인,Lugha in enumerate(('java','c','python')):
        faili_Orodha=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Lugha).iterdir()) if 자료위치.is_file()]
        if Lugha=='java':faili_Orodha += [(자료위치.stem+'.class',tabaka_njia/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        agizo_MFUATANO += ['if(Lugha==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Lugha]
        for Jina,njia in faili_Orodha:
            maudhui_thamani=guest_bytes(njia);lengo='/example/'+Lugha+'/'+Jina
            if len(maudhui_thamani)>16384 or len(lengo.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+lengo)
            agizo_MFUATANO.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(lengo,ensure_ascii=True),maudhui_thamani.hex()))
            꾸러미명세[lengo]={'bytes':len(maudhui_thamani),'sha256':hashlib.sha256(maudhui_thamani).hexdigest()}
        agizo_MFUATANO += ['return 0;}']
    agizo_MFUATANO += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(agizo_MFUATANO)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
