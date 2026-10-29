"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(ფესვი_მდებარეობა, 저장소경로, შესრულება_ბრძანება):
    원본자료=저장소경로/'example';გაზომვა_მონაცემები=ფესვი_მდებარეობა/'build/examples';გაზომვა_მონაცემები.mkdir(parents=True,exist_ok=True)
    კლასი_მდებარეობა=გაზომვა_მონაცემები/'classes';კლასი_მდებარეობა.mkdir(exist_ok=True)
    자바라이브러리만들기(ფესვი_მდებარეობა,შესრულება_ბრძანება)
    ip_settings = read_config(ფესვი_მდებარეობა)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = გაზომვა_მონაცემები/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    შესრულება_ბრძანება(['javac','--release','8','-encoding','UTF-8','-cp',ფესვი_მდებარეობა/'build/java-library/classes','-d',კლასი_მდებარეობა]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int ინსტალაცია_მნიშვნელობა(int ენა) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    წასაკითხი_ფაილი=guest_bytes(원본자료/'README.md')
    if len(წასაკითხი_ფაილი)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%წასაკითხი_ფაილი.hex())
    꾸러미명세['/example/README.md']={'bytes':len(წასაკითხი_ფაილი),'sha256':hashlib.sha256(წასაკითხი_ფაილი).hexdigest()}
    명령열.append('if(ენა==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for გეზი in [원본자료/'python/한국어.py'] + sorted((ფესვი_მდებარეობა/'파이썬연결/ბიბლიოთეკა').glob('*.py')):
        შიგთავსი_მნიშვნელობა=guest_bytes(გეზი);მიზანი='/lib/'+გეზი.name
        if len(შიგთავსი_მნიშვნელობა)>16384: raise ValueError('Python library exceeds native VFS limit: '+მიზანი)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(მიზანი,ensure_ascii=True),შიგთავსი_მნიშვნელობა.hex()))
        꾸러미명세[მიზანი]={'bytes':len(შიგთავსი_მნიშვნელობა),'sha256':hashlib.sha256(შიგთავსი_მნიშვნელობა).hexdigest()}
    명령열.append('}')
    for ძებნა_ინდექსი,ენა in enumerate(('java','c','python')):
        ფაილი_სია=[(მონაცემები_პოზიცია.name,მონაცემები_პოზიცია) for მონაცემები_პოზიცია in sorted((원본자료/ენა).iterdir()) if მონაცემები_პოზიცია.is_file()]
        if ენა=='java':ფაილი_სია += [(მონაცემები_პოზიცია.stem+'.class',კლასი_მდებარეობა/(მონაცემები_პოზიცია.stem+'.class')) for მონაცემები_პოზიცია in 자바실행]
        명령열 += ['if(ენა==%d){'%ძებნა_ინდექსი,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%ენა]
        for სახელი,გეზი in ფაილი_სია:
            შიგთავსი_მნიშვნელობა=guest_bytes(გეზი);მიზანი='/example/'+ენა+'/'+სახელი
            if len(შიგთავსი_მნიშვნელობა)>16384 or len(მიზანი.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+მიზანი)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(მიზანი,ensure_ascii=True),შიგთავსი_მნიშვნელობა.hex()))
            꾸러미명세[მიზანი]={'bytes':len(შიგთავსი_მნიშვნელობა),'sha256':hashlib.sha256(შიგთავსი_მნიშვნელობა).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (ფესვი_მდებარეობა/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (გაზომვა_მონაცემები/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
