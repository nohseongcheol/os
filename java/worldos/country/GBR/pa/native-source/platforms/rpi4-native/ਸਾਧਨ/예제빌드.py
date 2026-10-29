"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(ਰੂਟ_ਰਸਤਾ, 저장소경로, ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼):
    원본자료=저장소경로/'example';ਮਾਪ_ਸਮੱਗਰੀ=ਰੂਟ_ਰਸਤਾ/'build/examples';ਮਾਪ_ਸਮੱਗਰੀ.mkdir(parents=True,exist_ok=True)
    ਸ੍ਰੇਣੀ_ਰਸਤਾ=ਮਾਪ_ਸਮੱਗਰੀ/'classes';ਸ੍ਰੇਣੀ_ਰਸਤਾ.mkdir(exist_ok=True)
    자바라이브러리만들기(ਰੂਟ_ਰਸਤਾ,ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼)
    ip_settings = read_config(ਰੂਟ_ਰਸਤਾ)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = ਮਾਪ_ਸਮੱਗਰੀ/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(['javac','--release','8','-encoding','UTF-8','-cp',ਰੂਟ_ਰਸਤਾ/'build/java-library/classes','-d',ਸ੍ਰੇਣੀ_ਰਸਤਾ]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int ਸਥਾਪਿਤ_ਕਰੋ_ਕੀਮਤ(int ਭਾਸ਼ਾ) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ=guest_bytes(원본자료/'README.md')
    if len(ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ.hex())
    꾸러미명세['/example/README.md']={'bytes':len(ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ),'sha256':hashlib.sha256(ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ).hexdigest()}
    명령열.append('if(ਭਾਸ਼ਾ==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ਮਾਰਗ in [원본자료/'python/ਪੰਜਾਬੀ.py'] + sorted((ਰੂਟ_ਰਸਤਾ/'파이썬연결/ਪੁਸਤਕਾਲਾ').glob('*.py')):
        ਤਤਕਰਾ_ਕੀਮਤ=guest_bytes(ਮਾਰਗ);ਟੀਚਾ='/lib/'+ਮਾਰਗ.name
        if len(ਤਤਕਰਾ_ਕੀਮਤ)>16384: raise ValueError('Python library exceeds native VFS limit: '+ਟੀਚਾ)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ਟੀਚਾ,ensure_ascii=True),ਤਤਕਰਾ_ਕੀਮਤ.hex()))
        꾸러미명세[ਟੀਚਾ]={'bytes':len(ਤਤਕਰਾ_ਕੀਮਤ),'sha256':hashlib.sha256(ਤਤਕਰਾ_ਕੀਮਤ).hexdigest()}
    명령열.append('}')
    for ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ,ਭਾਸ਼ਾ in enumerate(('java','c','python')):
        ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ=[(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.name,ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ) for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in sorted((원본자료/ਭਾਸ਼ਾ).iterdir()) if ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.is_file()]
        if ਭਾਸ਼ਾ=='java':ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ += [(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stem+'.class',ਸ੍ਰੇਣੀ_ਰਸਤਾ/(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stem+'.class')) for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in 자바실행]
        명령열 += ['if(ਭਾਸ਼ਾ==%d){'%ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%ਭਾਸ਼ਾ]
        for ਨਾਂ,ਮਾਰਗ in ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ:
            ਤਤਕਰਾ_ਕੀਮਤ=guest_bytes(ਮਾਰਗ);ਟੀਚਾ='/example/'+ਭਾਸ਼ਾ+'/'+ਨਾਂ
            if len(ਤਤਕਰਾ_ਕੀਮਤ)>16384 or len(ਟੀਚਾ.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ਟੀਚਾ)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ਟੀਚਾ,ensure_ascii=True),ਤਤਕਰਾ_ਕੀਮਤ.hex()))
            꾸러미명세[ਟੀਚਾ]={'bytes':len(ਤਤਕਰਾ_ਕੀਮਤ),'sha256':hashlib.sha256(ਤਤਕਰਾ_ਕੀਮਤ).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (ਰੂਟ_ਰਸਤਾ/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (ਮਾਪ_ਸਮੱਗਰੀ/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
