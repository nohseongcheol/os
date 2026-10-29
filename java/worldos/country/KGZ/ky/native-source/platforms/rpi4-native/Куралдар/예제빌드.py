"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, аткаруу_буйрук):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    класс_жол=결과자료/'classes';класс_жол.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,аткаруу_буйрук)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    аткаруу_буйрук(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',класс_жол]+자바실행)
    аткаруу_буйругу_ЫРААТТУУЛУК=['public final class 예제꾸러미 { public static int орнотуу_маани(int Тил) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    readme_файл=guest_bytes(원본자료/'README.md')
    if len(readme_файл)>16384: raise ValueError('example README exceeds native VFS limit')
    аткаруу_буйругу_ЫРААТТУУЛУК.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%readme_файл.hex())
    꾸러미명세['/example/README.md']={'bytes':len(readme_файл),'sha256':hashlib.sha256(readme_файл).hexdigest()}
    аткаруу_буйругу_ЫРААТТУУЛУК.append('if(Тил==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ЖОЛ in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/жыйнак').glob('*.py')):
        Мазмун_маани=guest_bytes(ЖОЛ);максат='/lib/'+ЖОЛ.name
        if len(Мазмун_маани)>16384: raise ValueError('Python library exceeds native VFS limit: '+максат)
        аткаруу_буйругу_ЫРААТТУУЛУК.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(максат,ensure_ascii=True),Мазмун_маани.hex()))
        꾸러미명세[максат]={'bytes':len(Мазмун_маани),'sha256':hashlib.sha256(Мазмун_маани).hexdigest()}
    аткаруу_буйругу_ЫРААТТУУЛУК.append('}')
    for 색인,Тил in enumerate(('java','c','python')):
        файл_Тизме=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Тил).iterdir()) if 자료위치.is_file()]
        if Тил=='java':файл_Тизме += [(자료위치.stem+'.class',класс_жол/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        аткаруу_буйругу_ЫРААТТУУЛУК += ['if(Тил==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Тил]
        for Аты,ЖОЛ in файл_Тизме:
            Мазмун_маани=guest_bytes(ЖОЛ);максат='/example/'+Тил+'/'+Аты
            if len(Мазмун_маани)>16384 or len(максат.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+максат)
            аткаруу_буйругу_ЫРААТТУУЛУК.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(максат,ensure_ascii=True),Мазмун_маани.hex()))
            꾸러미명세[максат]={'bytes':len(Мазмун_маани),'sha256':hashlib.sha256(Мазмун_маани).hexdigest()}
        аткаруу_буйругу_ЫРААТТУУЛУК += ['return 0;}']
    аткаруу_буйругу_ЫРААТТУУЛУК += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(аткаруу_буйругу_ЫРААТТУУЛУК)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
