"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(בסיס_נתיב, מאגר_נתיב, לבצע_פקודה):
    원본자료=מאגר_נתיב/'example';תוצאה_נתונים=בסיס_נתיב/'build/examples';תוצאה_נתונים.mkdir(parents=True,exist_ok=True)
    כיתה_נתיב=תוצאה_נתונים/'classes';כיתה_נתיב.mkdir(exist_ok=True)
    자바라이브러리만들기(בסיס_נתיב,לבצע_פקודה)
    ip_settings = read_config(בסיס_נתיב)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = תוצאה_נתונים/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    לבצע_פקודה(['javac','--release','8','-encoding','UTF-8','-cp',בסיס_נתיב/'build/java-library/classes','-d',כיתה_נתיב]+자바실행)
    הוראה_רצף=['public final class 예제꾸러미 { public static int התקן_ערך(int שפה) { int 처리값;',
          '처리값=מפרשפקודות.예제폴더("/example"); if(처리값<0)return 처리값;']
    חבילה_מניפסט={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    הוראה_רצף.append('처리값=מפרשפקודות.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    חבילה_מניפסט['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    הוראה_רצף.append('if(שפה==0){처리값=מפרשפקודות.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for נתיב in [원본자료/'python/עברית.py'] + sorted((בסיס_נתיב/'파이썬연결/ספריה').glob('*.py')):
        תוכן_ערך=guest_bytes(נתיב);יעד='/lib/'+נתיב.name
        if len(תוכן_ערך)>16384: raise ValueError('Python library exceeds native VFS limit: '+יעד)
        הוראה_רצף.append('처리값=מפרשפקודות.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(יעד,ensure_ascii=True),תוכן_ערך.hex()))
        חבילה_מניפסט[יעד]={'bytes':len(תוכן_ערך),'sha256':hashlib.sha256(תוכן_ערך).hexdigest()}
    הוראה_רצף.append('}')
    for חפושׂ_מדד,שפה in enumerate(('java','c','python')):
        קובץ_רשימה=[(נתונים_עמדה.name,נתונים_עמדה) for נתונים_עמדה in sorted((원본자료/שפה).iterdir()) if נתונים_עמדה.is_file()]
        if שפה=='java':קובץ_רשימה += [(נתונים_עמדה.stem+'.class',כיתה_נתיב/(נתונים_עמדה.stem+'.class')) for נתונים_עמדה in 자바실행]
        הוראה_רצף += ['if(שפה==%d){'%חפושׂ_מדד,'처리값=מפרשפקודות.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%שפה]
        for שם,נתיב in קובץ_רשימה:
            תוכן_ערך=guest_bytes(נתיב);יעד='/example/'+שפה+'/'+שם
            if len(תוכן_ערך)>16384 or len(יעד.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+יעד)
            הוראה_רצף.append('처리값=מפרשפקודות.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(יעד,ensure_ascii=True),תוכן_ערך.hex()))
            חבילה_מניפסט[יעד]={'bytes':len(תוכן_ערך),'sha256':hashlib.sha256(תוכן_ערך).hexdigest()}
        הוראה_רצף += ['return 0;}']
    הוראה_רצף += ['return -22;}}']
    (בסיס_נתיב/'build/예제꾸러미.java').write_text('\n'.join(הוראה_רצף)+'\n')
    (תוצאה_נתונים/'manifest.json').write_text(json.dumps(חבילה_מניפסט,ensure_ascii=False,indent=2)+'\n')
