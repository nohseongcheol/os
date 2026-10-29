"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(جذر_مسیر, مخزن_مسیر, اجرا_فرمان):
    원본자료=مخزن_مسیر/'example';سنجش_داده_ها=جذر_مسیر/'build/examples';سنجش_داده_ها.mkdir(parents=True,exist_ok=True)
    کلاس_مسیر=سنجش_داده_ها/'classes';کلاس_مسیر.mkdir(exist_ok=True)
    자바라이브러리만들기(جذر_مسیر,اجرا_فرمان)
    ip_settings = read_config(جذر_مسیر)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = سنجش_داده_ها/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    اجرا_فرمان(['javac','--release','8','-encoding','UTF-8','-cp',جذر_مسیر/'build/java-library/classes','-d',کلاس_مسیر]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int نصب_مقدار(int زبان) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    مرا_بخوان=guest_bytes(원본자료/'README.md')
    if len(مرا_بخوان)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%مرا_بخوان.hex())
    꾸러미명세['/example/README.md']={'bytes':len(مرا_بخوان),'sha256':hashlib.sha256(مرا_بخوان).hexdigest()}
    명령열.append('if(زبان==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for مسیر in [원본자료/'python/فارسی.py'] + sorted((جذر_مسیر/'파이썬연결/کتابخانه').glob('*.py')):
        محتوا_مقدار=guest_bytes(مسیر);هدف='/lib/'+مسیر.name
        if len(محتوا_مقدار)>16384: raise ValueError('Python library exceeds native VFS limit: '+هدف)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(هدف,ensure_ascii=True),محتوا_مقدار.hex()))
        꾸러미명세[هدف]={'bytes':len(محتوا_مقدار),'sha256':hashlib.sha256(محتوا_مقدار).hexdigest()}
    명령열.append('}')
    for جستجو_فهرست,زبان in enumerate(('java','c','python')):
        فایل_لیست=[(داده_ها_مرتب_کردن.name,داده_ها_مرتب_کردن) for داده_ها_مرتب_کردن in sorted((원본자료/زبان).iterdir()) if داده_ها_مرتب_کردن.is_file()]
        if زبان=='java':فایل_لیست += [(داده_ها_مرتب_کردن.stem+'.class',کلاس_مسیر/(داده_ها_مرتب_کردن.stem+'.class')) for داده_ها_مرتب_کردن in 자바실행]
        명령열 += ['if(زبان==%d){'%جستجو_فهرست,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%زبان]
        for نام,مسیر in فایل_لیست:
            محتوا_مقدار=guest_bytes(مسیر);هدف='/example/'+زبان+'/'+نام
            if len(محتوا_مقدار)>16384 or len(هدف.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+هدف)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(هدف,ensure_ascii=True),محتوا_مقدار.hex()))
            꾸러미명세[هدف]={'bytes':len(محتوا_مقدار),'sha256':hashlib.sha256(محتوا_مقدار).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (جذر_مسیر/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (سنجش_داده_ها/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
