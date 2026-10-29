"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(جذر_مسار, مستودع_مسار, ينفذ_أمر):
    원본자료=مستودع_مسار/'example';مقياس_بيانات=جذر_مسار/'build/examples';مقياس_بيانات.mkdir(parents=True,exist_ok=True)
    فئة_مسار=مقياس_بيانات/'classes';فئة_مسار.mkdir(exist_ok=True)
    자바라이브러리만들기(جذر_مسار,ينفذ_أمر)
    ip_settings = read_config(جذر_مسار)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = مقياس_بيانات/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ينفذ_أمر(['javac','--release','8','-encoding','UTF-8','-cp',جذر_مسار/'build/java-library/classes','-d',فئة_مسار]+자바실행)
    تعليمة_تسلسل=['public final class 예제꾸러미 { public static int تثبيت_قيمة(int لغة) { int 처리값;',
          '처리값=مفسر_الأوامر.예제폴더("/example"); if(처리값<0)return 처리값;']
    يُجمع_بيان={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    تعليمة_تسلسل.append('처리값=مفسر_الأوامر.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    يُجمع_بيان['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    تعليمة_تسلسل.append('if(لغة==0){처리값=مفسر_الأوامر.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for مسار in [원본자료/'python/العربية.py'] + sorted((جذر_مسار/'파이썬연결/مكتبة').glob('*.py')):
        محتوى_قيمة=guest_bytes(مسار);الهدف='/lib/'+مسار.name
        if len(محتوى_قيمة)>16384 or len(الهدف.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+الهدف)
        تعليمة_تسلسل.append('처리값=مفسر_الأوامر.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(الهدف,ensure_ascii=True),محتوى_قيمة.hex()))
        يُجمع_بيان[الهدف]={'bytes':len(محتوى_قيمة),'sha256':hashlib.sha256(محتوى_قيمة).hexdigest()}
    تعليمة_تسلسل.append('}')
    for البحث_فهرس,لغة in enumerate(('java','c','python')):
        ملف_قائمة=[(بيانات_منصب.name,بيانات_منصب) for بيانات_منصب in sorted((원본자료/لغة).iterdir()) if بيانات_منصب.is_file()]
        if لغة=='java':ملف_قائمة += [(بيانات_منصب.stem+'.class',فئة_مسار/(بيانات_منصب.stem+'.class')) for بيانات_منصب in 자바실행]
        تعليمة_تسلسل += ['if(لغة==%d){'%البحث_فهرس,'처리값=مفسر_الأوامر.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%لغة]
        for اسم,مسار in ملف_قائمة:
            محتوى_قيمة=guest_bytes(مسار);الهدف='/example/'+لغة+'/'+اسم
            if len(محتوى_قيمة)>16384 or len(الهدف.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+الهدف)
            تعليمة_تسلسل.append('처리값=مفسر_الأوامر.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(الهدف,ensure_ascii=True),محتوى_قيمة.hex()))
            يُجمع_بيان[الهدف]={'bytes':len(محتوى_قيمة),'sha256':hashlib.sha256(محتوى_قيمة).hexdigest()}
        تعليمة_تسلسل += ['return 0;}']
    تعليمة_تسلسل += ['return -22;}}']
    (جذر_مسار/'build/예제꾸러미.java').write_text('\n'.join(تعليمة_تسلسل)+'\n')
    (مقياس_بيانات/'manifest.json').write_text(json.dumps(يُجمع_بيان,ensure_ascii=False,indent=2)+'\n')
