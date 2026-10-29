"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(արմատ_ուղի, 저장소경로, կատարել_հրաման):
    원본자료=저장소경로/'example';չափ_տվյալ=արմատ_ուղի/'build/examples';չափ_տվյալ.mkdir(parents=True,exist_ok=True)
    դաս_ուղի=չափ_տվյալ/'classes';դաս_ուղի.mkdir(exist_ok=True)
    자바라이브러리만들기(արմատ_ուղի,կատարել_հրաման)
    ip_settings = read_config(արմատ_ուղի)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = չափ_տվյալ/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    կատարել_հրաման(['javac','--release','8','-encoding','UTF-8','-cp',արմատ_ուղի/'build/java-library/classes','-d',դաս_ուղի]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int տեղադրել_արժեք(int Լեզու) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    ԿԱՐԴԱ_ԻՆՁ=guest_bytes(원본자료/'README.md')
    if len(ԿԱՐԴԱ_ԻՆՁ)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%ԿԱՐԴԱ_ԻՆՁ.hex())
    꾸러미명세['/example/README.md']={'bytes':len(ԿԱՐԴԱ_ԻՆՁ),'sha256':hashlib.sha256(ԿԱՐԴԱ_ԻՆՁ).hexdigest()}
    명령열.append('if(Լեզու==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for Ճանապարհ in [원본자료/'python/한국어.py'] + sorted((արմատ_ուղի/'파이썬연결/դարան').glob('*.py')):
        Բովանդակություն_արժեք=guest_bytes(Ճանապարհ);թիրախ='/lib/'+Ճանապարհ.name
        if len(Բովանդակություն_արժեք)>16384: raise ValueError('Python library exceeds native VFS limit: '+թիրախ)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(թիրախ,ensure_ascii=True),Բովանդակություն_արժեք.hex()))
        꾸러미명세[թիրախ]={'bytes':len(Բովանդակություն_արժեք),'sha256':hashlib.sha256(Բովանդակություն_արժեք).hexdigest()}
    명령열.append('}')
    for Փնտրում_դասիչ,Լեզու in enumerate(('java','c','python')):
        նիշք_Ցուցակ=[(տվյալ_դիրք.name,տվյալ_դիրք) for տվյալ_դիրք in sorted((원본자료/Լեզու).iterdir()) if տվյալ_դիրք.is_file()]
        if Լեզու=='java':նիշք_Ցուցակ += [(տվյալ_դիրք.stem+'.class',դաս_ուղի/(տվյալ_դիրք.stem+'.class')) for տվյալ_դիրք in 자바실행]
        명령열 += ['if(Լեզու==%d){'%Փնտրում_դասիչ,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Լեզու]
        for Անուն,Ճանապարհ in նիշք_Ցուցակ:
            Բովանդակություն_արժեք=guest_bytes(Ճանապարհ);թիրախ='/example/'+Լեզու+'/'+Անուն
            if len(Բովանդակություն_արժեք)>16384 or len(թիրախ.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+թիրախ)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(թիրախ,ensure_ascii=True),Բովանդակություն_արժեք.hex()))
            꾸러미명세[թիրախ]={'bytes':len(Բովանդակություն_արժեք),'sha256':hashlib.sha256(Բովանդակություն_արժեք).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (արմատ_ուղի/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (չափ_տվյալ/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
