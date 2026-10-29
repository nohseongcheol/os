"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(ስር_ዱካ, ማከማቻ_ዱካ, ፈጽም_ትእዛዝ):
    원본자료=ማከማቻ_ዱካ/'example';ልኬት_ውሂብ=ስር_ዱካ/'build/examples';ልኬት_ውሂብ.mkdir(parents=True,exist_ok=True)
    መደብ_ዱካ=ልኬት_ውሂብ/'classes';መደብ_ዱካ.mkdir(exist_ok=True)
    자바라이브러리만들기(ስር_ዱካ,ፈጽም_ትእዛዝ)
    ip_settings = read_config(ስር_ዱካ)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = ልኬት_ውሂብ/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ፈጽም_ትእዛዝ(['javac','--release','8','-encoding','UTF-8','-cp',ስር_ዱካ/'build/java-library/classes','-d',መደብ_ዱካ]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int ጫን_እሴት(int ቋንቋ) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    አንበኝ=guest_bytes(원본자료/'README.md')
    if len(አንበኝ)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%አንበኝ.hex())
    꾸러미명세['/example/README.md']={'bytes':len(አንበኝ),'sha256':hashlib.sha256(አንበኝ).hexdigest()}
    명령열.append('if(ቋንቋ==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for መተላለፊያ in [원본자료/'python/አማርኛ.py'] + sorted((ስር_ዱካ/'파이썬연결/ማከማቻ_ስፍራ').glob('*.py')):
        ይዘት_እሴት=guest_bytes(መተላለፊያ);ዓላማ='/lib/'+መተላለፊያ.name
        if len(ይዘት_እሴት)>16384 or len(ዓላማ.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+ዓላማ)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ዓላማ,ensure_ascii=True),ይዘት_እሴት.hex()))
        꾸러미명세[ዓላማ]={'bytes':len(ይዘት_እሴት),'sha256':hashlib.sha256(ይዘት_እሴት).hexdigest()}
    명령열.append('}')
    for ፍለጋ_መረጃ_ጠቆመ,ቋንቋ in enumerate(('java','c','python')):
        ፋይል_ዝርዝር=[(ውሂብ_በቦታ_አስቀመጠ.name,ውሂብ_በቦታ_አስቀመጠ) for ውሂብ_በቦታ_አስቀመጠ in sorted((원본자료/ቋንቋ).iterdir()) if ውሂብ_በቦታ_አስቀመጠ.is_file()]
        if ቋንቋ=='java':ፋይል_ዝርዝር += [(ውሂብ_በቦታ_አስቀመጠ.stem+'.class',መደብ_ዱካ/(ውሂብ_በቦታ_አስቀመጠ.stem+'.class')) for ውሂብ_በቦታ_አስቀመጠ in 자바실행]
        명령열 += ['if(ቋንቋ==%d){'%ፍለጋ_መረጃ_ጠቆመ,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%ቋንቋ]
        for ስም,መተላለፊያ in ፋይል_ዝርዝር:
            ይዘት_እሴት=guest_bytes(መተላለፊያ);ዓላማ='/example/'+ቋንቋ+'/'+ስም
            if len(ይዘት_እሴት)>16384 or len(ዓላማ.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ዓላማ)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ዓላማ,ensure_ascii=True),ይዘት_እሴት.hex()))
            꾸러미명세[ዓላማ]={'bytes':len(ይዘት_እሴት),'sha256':hashlib.sha256(ይዘት_እሴት).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (ስር_ዱካ/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (ልኬት_ውሂብ/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
