"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(يىلتىز_يول, 저장소경로, ئىجرا_قىلىش_بۇيرۇق):
    원본자료=저장소경로/'example';ئۆلچەم_مەلۇمات=يىلتىز_يول/'build/examples';ئۆلچەم_مەلۇمات.mkdir(parents=True,exist_ok=True)
    تۈركۈم_يول=ئۆلچەم_مەلۇمات/'classes';تۈركۈم_يول.mkdir(exist_ok=True)
    자바라이브러리만들기(يىلتىز_يول,ئىجرا_قىلىش_بۇيرۇق)
    ip_settings = read_config(يىلتىز_يول)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = ئۆلچەم_مەلۇمات/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ئىجرا_قىلىش_بۇيرۇق(['javac','--release','8','-encoding','UTF-8','-cp',يىلتىز_يول/'build/java-library/classes','-d',تۈركۈم_يول]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int قاچىلاش_قىممىتى(int تىل) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    چۈشەندۈرۈش_ھۆججىتى=guest_bytes(원본자료/'README.md')
    if len(چۈشەندۈرۈش_ھۆججىتى)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%چۈشەندۈرۈش_ھۆججىتى.hex())
    꾸러미명세['/example/README.md']={'bytes':len(چۈشەندۈرۈش_ھۆججىتى),'sha256':hashlib.sha256(چۈشەندۈرۈش_ھۆججىتى).hexdigest()}
    명령열.append('if(تىل==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for يول in [원본자료/'python/한국어.py'] + sorted((يىلتىز_يول/'파이썬연결/ئامبار').glob('*.py')):
        مەزمۇن_قىممىتى=guest_bytes(يول);نىشان='/lib/'+يول.name
        if len(مەزمۇن_قىممىتى)>16384: raise ValueError('Python library exceeds native VFS limit: '+نىشان)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(نىشان,ensure_ascii=True),مەزمۇن_قىممىتى.hex()))
        꾸러미명세[نىشان]={'bytes':len(مەزمۇن_قىممىتى),'sha256':hashlib.sha256(مەزمۇن_قىممىتى).hexdigest()}
    명령열.append('}')
    for ئىزدەش_ئىندېكس,تىل in enumerate(('java','c','python')):
        ھۆججەت_تىزىم=[(مەلۇمات_ئورۇنلاشتۇرۇش.name,مەلۇمات_ئورۇنلاشتۇرۇش) for مەلۇمات_ئورۇنلاشتۇرۇش in sorted((원본자료/تىل).iterdir()) if مەلۇمات_ئورۇنلاشتۇرۇش.is_file()]
        if تىل=='java':ھۆججەت_تىزىم += [(مەلۇمات_ئورۇنلاشتۇرۇش.stem+'.class',تۈركۈم_يول/(مەلۇمات_ئورۇنلاشتۇرۇش.stem+'.class')) for مەلۇمات_ئورۇنلاشتۇرۇش in 자바실행]
        명령열 += ['if(تىل==%d){'%ئىزدەش_ئىندېكس,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%تىل]
        for ئاتى,يول in ھۆججەت_تىزىم:
            مەزمۇن_قىممىتى=guest_bytes(يول);نىشان='/example/'+تىل+'/'+ئاتى
            if len(مەزمۇن_قىممىتى)>16384 or len(نىشان.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+نىشان)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(نىشان,ensure_ascii=True),مەزمۇن_قىممىتى.hex()))
            꾸러미명세[نىشان]={'bytes':len(مەزمۇن_قىممىتى),'sha256':hashlib.sha256(مەزمۇن_قىممىتى).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (يىلتىز_يول/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (ئۆلچەم_مەلۇمات/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
