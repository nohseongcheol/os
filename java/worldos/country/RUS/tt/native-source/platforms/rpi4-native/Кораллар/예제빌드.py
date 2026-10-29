"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(тамыр_юл, 저장소경로, үтәргә_команда):
    원본자료=저장소경로/'example';үлчәм_мәгълүмат=тамыр_юл/'build/examples';үлчәм_мәгълүмат.mkdir(parents=True,exist_ok=True)
    класс_юл=үлчәм_мәгълүмат/'classes';класс_юл.mkdir(exist_ok=True)
    자바라이브러리만들기(тамыр_юл,үтәргә_команда)
    ip_settings = read_config(тамыр_юл)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = үлчәм_мәгълүмат/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    үтәргә_команда(['javac','--release','8','-encoding','UTF-8','-cp',тамыр_юл/'build/java-library/classes','-d',класс_юл]+자바실행)
    инструкция_SEQUENCE=['public final class 예제꾸러미 { public static int урнаштыру_VALUE_6a28baa5(int тел) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    Белешмә_файлы=guest_bytes(원본자료/'README.md')
    if len(Белешмә_файлы)>16384: raise ValueError('example README exceeds native VFS limit')
    инструкция_SEQUENCE.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%Белешмә_файлы.hex())
    꾸러미명세['/example/README.md']={'bytes':len(Белешмә_файлы),'sha256':hashlib.sha256(Белешмә_файлы).hexdigest()}
    инструкция_SEQUENCE.append('if(тел==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for Yul in [원본자료/'python/Татарча.py'] + sorted((тамыр_юл/'PYTHON_күпер/библиотека').glob('*.py')):
        Эчтәлек_VALUE=guest_bytes(Yul);максат_кыйммәт='/lib/'+Yul.name
        if len(Эчтәлек_VALUE)>16384: raise ValueError('Python library exceeds native VFS limit: '+максат_кыйммәт)
        инструкция_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(максат_кыйммәт,ensure_ascii=True),Эчтәлек_VALUE.hex()))
        꾸러미명세[максат_кыйммәт]={'bytes':len(Эчтәлек_VALUE),'sha256':hashlib.sha256(Эчтәлек_VALUE).hexdigest()}
    инструкция_SEQUENCE.append('}')
    for Эзләү_INDEX,тел in enumerate(('java','c','python')):
        файл_Исемлек=[(мәгълүмат_урнаштыру.name,мәгълүмат_урнаштыру) for мәгълүмат_урнаштыру in sorted((원본자료/тел).iterdir()) if мәгълүмат_урнаштыру.is_file()]
        if тел=='java':файл_Исемлек += [(мәгълүмат_урнаштыру.stem+'.class',класс_юл/(мәгълүмат_урнаштыру.stem+'.class')) for мәгълүмат_урнаштыру in 자바실행]
        инструкция_SEQUENCE += ['if(тел==%d){'%Эзләү_INDEX,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%тел]
        for исем,Yul in файл_Исемлек:
            Эчтәлек_VALUE=guest_bytes(Yul);максат_кыйммәт='/example/'+тел+'/'+исем
            if len(Эчтәлек_VALUE)>16384 or len(максат_кыйммәт.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+максат_кыйммәт)
            инструкция_SEQUENCE.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(максат_кыйммәт,ensure_ascii=True),Эчтәлек_VALUE.hex()))
            꾸러미명세[максат_кыйммәт]={'bytes':len(Эчтәлек_VALUE),'sha256':hashlib.sha256(Эчтәлек_VALUE).hexdigest()}
        инструкция_SEQUENCE += ['return 0;}']
    инструкция_SEQUENCE += ['return -22;}}']
    (тамыр_юл/'build/예제꾸러미.java').write_text('\n'.join(инструкция_SEQUENCE)+'\n')
    (үлчәм_мәгълүмат/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
