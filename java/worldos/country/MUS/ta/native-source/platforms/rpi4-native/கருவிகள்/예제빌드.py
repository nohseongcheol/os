"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(மூலம்_பாதை, தொகுபதிவகம்_பாதை, இயக்கு_கட்டளை):
    원본자료=தொகுபதிவகம்_பாதை/'example';அளவிடக்கூடியது_தரவு=மூலம்_பாதை/'build/examples';அளவிடக்கூடியது_தரவு.mkdir(parents=True,exist_ok=True)
    பிரிவு_பாதை=அளவிடக்கூடியது_தரவு/'classes';பிரிவு_பாதை.mkdir(exist_ok=True)
    자바라이브러리만들기(மூலம்_பாதை,இயக்கு_கட்டளை)
    ip_settings = read_config(மூலம்_பாதை)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = அளவிடக்கூடியது_தரவு/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    இயக்கு_கட்டளை(['javac','--release','8','-encoding','UTF-8','-cp',மூலம்_பாதை/'build/java-library/classes','-d',பிரிவு_பாதை]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int நிறுவு_மதிப்பு(int மொழி) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    மூட்டை_தொற்றம்={}
    பயனர்_உதவிக்_கோப்பு=guest_bytes(원본자료/'README.md')
    if len(பயனர்_உதவிக்_கோப்பு)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%பயனர்_உதவிக்_கோப்பு.hex())
    மூட்டை_தொற்றம்['/example/README.md']={'bytes':len(பயனர்_உதவிக்_கோப்பு),'sha256':hashlib.sha256(பயனர்_உதவிக்_கோப்பு).hexdigest()}
    명령열.append('if(மொழி==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for பாதை_2 in [원본자료/'python/தமிழ்.py'] + sorted((மூலம்_பாதை/'파이썬연결/நூலகம்').glob('*.py')):
        உள்ளடக்கம்_மதிப்பு=guest_bytes(பாதை_2);இலக்கு='/lib/'+பாதை_2.name
        if len(உள்ளடக்கம்_மதிப்பு)>16384: raise ValueError('Python library exceeds native VFS limit: '+இலக்கு)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(இலக்கு,ensure_ascii=True),உள்ளடக்கம்_மதிப்பு.hex()))
        மூட்டை_தொற்றம்[இலக்கு]={'bytes':len(உள்ளடக்கம்_மதிப்பு),'sha256':hashlib.sha256(உள்ளடக்கம்_மதிப்பு).hexdigest()}
    명령열.append('}')
    for தேடுதல்_அடைவு,மொழி in enumerate(('java','c','python')):
        கோப்பு_பட்டியல்=[(தரவு_நிலை.name,தரவு_நிலை) for தரவு_நிலை in sorted((원본자료/மொழி).iterdir()) if தரவு_நிலை.is_file()]
        if மொழி=='java':கோப்பு_பட்டியல் += [(தரவு_நிலை.stem+'.class',பிரிவு_பாதை/(தரவு_நிலை.stem+'.class')) for தரவு_நிலை in 자바실행]
        명령열 += ['if(மொழி==%d){'%தேடுதல்_அடைவு,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%மொழி]
        for பெயர்,பாதை_2 in கோப்பு_பட்டியல்:
            உள்ளடக்கம்_மதிப்பு=guest_bytes(பாதை_2);இலக்கு='/example/'+மொழி+'/'+பெயர்
            if len(உள்ளடக்கம்_மதிப்பு)>16384 or len(இலக்கு.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+இலக்கு)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(இலக்கு,ensure_ascii=True),உள்ளடக்கம்_மதிப்பு.hex()))
            மூட்டை_தொற்றம்[இலக்கு]={'bytes':len(உள்ளடக்கம்_மதிப்பு),'sha256':hashlib.sha256(உள்ளடக்கம்_மதிப்பு).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (மூலம்_பாதை/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (அளவிடக்கூடியது_தரவு/'manifest.json').write_text(json.dumps(மூட்டை_தொற்றம்,ensure_ascii=False,indent=2)+'\n')
