"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(корень_путь, репозиторий_путь, 실행):
    원본자료=репозиторий_путь/'example';KR_данные=корень_путь/'build/examples';KR_данные.mkdir(parents=True,exist_ok=True)
    Класс_путь=KR_данные/'classes';Класс_путь.mkdir(exist_ok=True)
    자바라이브러리만들기(корень_путь,실행)
    ip_settings = read_config(корень_путь)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KR_данные/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    실행(['javac','--release','8','-encoding','UTF-8','-cp',корень_путь/'build/java-library/classes','-d',Класс_путь]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int установить_ЗНАЧЕН(int Язык) { int 처리값;',
          '처리값=ИнтерпретаторКоманд.예제폴더("/example"); if(처리값<0)return 처리값;']
    пакет_манифест={}
    файл_сведений=guest_bytes(원본자료/'README.md')
    if len(файл_сведений)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=ИнтерпретаторКоманд.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%файл_сведений.hex())
    пакет_манифест['/example/README.md']={'bytes':len(файл_сведений),'sha256':hashlib.sha256(файл_сведений).hexdigest()}
    명령열.append('if(Язык==0){처리값=ИнтерпретаторКоманд.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for путь in [원본자료/'python/русский.py'] + sorted((корень_путь/'PYTHON_мост/библиотека').glob('*.py')):
        контент_ЗНАЧЕН=guest_bytes(путь);целевое_значение='/lib/'+путь.name
        if len(контент_ЗНАЧЕН)>16384 or len(целевое_значение.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+целевое_значение)
        명령열.append('처리값=ИнтерпретаторКоманд.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(целевое_значение,ensure_ascii=True),контент_ЗНАЧЕН.hex()))
        пакет_манифест[целевое_значение]={'bytes':len(контент_ЗНАЧЕН),'sha256':hashlib.sha256(контент_ЗНАЧЕН).hexdigest()}
    명령열.append('}')
    for Поиск_ИНДЕКС,Язык in enumerate(('java','c','python')):
        список_файлов=[(данные_позиция.name,данные_позиция) for данные_позиция in sorted((원본자료/Язык).iterdir()) if данные_позиция.is_file()]
        if Язык=='java':список_файлов += [(данные_позиция.stem+'.class',Класс_путь/(данные_позиция.stem+'.class')) for данные_позиция in 자바실행]
        명령열 += ['if(Язык==%d){'%Поиск_ИНДЕКС,'처리값=ИнтерпретаторКоманд.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Язык]
        for Название,путь in список_файлов:
            контент_ЗНАЧЕН=guest_bytes(путь);целевое_значение='/example/'+Язык+'/'+Название
            if len(контент_ЗНАЧЕН)>16384 or len(целевое_значение.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+целевое_значение)
            명령열.append('처리값=ИнтерпретаторКоманд.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(целевое_значение,ensure_ascii=True),контент_ЗНАЧЕН.hex()))
            пакет_манифест[целевое_значение]={'bytes':len(контент_ЗНАЧЕН),'sha256':hashlib.sha256(контент_ЗНАЧЕН).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (корень_путь/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (KR_данные/'manifest.json').write_text(json.dumps(пакет_манифест,ensure_ascii=False,indent=2)+'\n')
