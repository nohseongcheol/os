"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, جێبەجێکردن_فەرمان):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    کلاس_گوزەر=결과자료/'classes';کلاس_گوزەر.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,جێبەجێکردن_فەرمان)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    جێبەجێکردن_فەرمان(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',کلاس_گوزەر]+자바실행)
    ڕێنمایی_زنجیره=['public final class 예제꾸러미 { public static int دامەزرێنە_نرخ(int زمان) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    رێخۆشکەر=guest_bytes(원본자료/'README.md')
    if len(رێخۆشکەر)>16384: raise ValueError('example README exceeds native VFS limit')
    ڕێنمایی_زنجیره.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%رێخۆشکەر.hex())
    꾸러미명세['/example/README.md']={'bytes':len(رێخۆشکەر),'sha256':hashlib.sha256(رێخۆشکەر).hexdigest()}
    ڕێنمایی_زنجیره.append('if(زمان==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for گوزەر in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/کتێبخانە').glob('*.py')):
        ناوەرۆک_نرخ=guest_bytes(گوزەر);مەبەست='/lib/'+گوزەر.name
        if len(ناوەرۆک_نرخ)>16384 or len(مەبەست.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+مەبەست)
        ڕێنمایی_زنجیره.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(مەبەست,ensure_ascii=True),ناوەرۆک_نرخ.hex()))
        꾸러미명세[مەبەست]={'bytes':len(ناوەرۆک_نرخ),'sha256':hashlib.sha256(ناوەرۆک_نرخ).hexdigest()}
    ڕێنمایی_زنجیره.append('}')
    for 색인,زمان in enumerate(('java','c','python')):
        فایل_لیست=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/زمان).iterdir()) if 자료위치.is_file()]
        if زمان=='java':فایل_لیست += [(자료위치.stem+'.class',کلاس_گوزەر/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        ڕێنمایی_زنجیره += ['if(زمان==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%زمان]
        for ناو,گوزەر in فایل_لیست:
            ناوەرۆک_نرخ=guest_bytes(گوزەر);مەبەست='/example/'+زمان+'/'+ناو
            if len(ناوەرۆک_نرخ)>16384 or len(مەبەست.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+مەبەست)
            ڕێنمایی_زنجیره.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(مەبەست,ensure_ascii=True),ناوەرۆک_نرخ.hex()))
            꾸러미명세[مەبەست]={'bytes':len(ناوەرۆک_نرخ),'sha256':hashlib.sha256(ناوەرۆک_نرخ).hexdigest()}
        ڕێنمایی_زنجیره += ['return 0;}']
    ڕێنمایی_زنجیره += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(ڕێنمایی_زنجیره)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
