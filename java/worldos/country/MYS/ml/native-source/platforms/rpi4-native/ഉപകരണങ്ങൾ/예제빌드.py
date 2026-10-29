"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(വർഗ്ഗമൂലം_പാത, കലവറ_പാത, നടപ്പാക്കുക_കമാന്_ഡ്):
    원본자료=കലവറ_പാത/'example';അളവ്_ഡാറ്റാ=വർഗ്ഗമൂലം_പാത/'build/examples';അളവ്_ഡാറ്റാ.mkdir(parents=True,exist_ok=True)
    ക്ലാസ്_പാത=അളവ്_ഡാറ്റാ/'classes';ക്ലാസ്_പാത.mkdir(exist_ok=True)
    자바라이브러리만들기(വർഗ്ഗമൂലം_പാത,നടപ്പാക്കുക_കമാന്_ഡ്)
    ip_settings = read_config(വർഗ്ഗമൂലം_പാത)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = അളവ്_ഡാറ്റാ/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    നടപ്പാക്കുക_കമാന്_ഡ്(['javac','--release','8','-encoding','UTF-8','-cp',വർഗ്ഗമൂലം_പാത/'build/java-library/classes','-d',ക്ലാസ്_പാത]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int ഇന്_സ്റ്റാള്_ചെയ്യുക_മൂല്യം(int భాష) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    ബണ്ടിൽ_ആവിഷ്കാരം={}
    readme_ഫയല്=guest_bytes(원본자료/'README.md')
    if len(readme_ഫയല്)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%readme_ഫയല്.hex())
    ബണ്ടിൽ_ആവിഷ്കാരം['/example/README.md']={'bytes':len(readme_ഫയല്),'sha256':hashlib.sha256(readme_ഫയല്).hexdigest()}
    명령열.append('if(భాష==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for വഴി in [원본자료/'python/한국어.py'] + sorted((വർഗ്ഗമൂലം_പാത/'파이썬연결/లైబ్రరీ').glob('*.py')):
        ഉള്ളടക്കം_മൂല്യം=guest_bytes(വഴി);ലക്_ഷ്യം='/lib/'+വഴി.name
        if len(ഉള്ളടക്കം_മൂല്യം)>16384: raise ValueError('Python library exceeds native VFS limit: '+ലക്_ഷ്യം)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ലക്_ഷ്യം,ensure_ascii=True),ഉള്ളടക്കം_മൂല്യം.hex()))
        ബണ്ടിൽ_ആവിഷ്കാരം[ലക്_ഷ്യം]={'bytes':len(ഉള്ളടക്കം_മൂല്യം),'sha256':hashlib.sha256(ഉള്ളടക്കം_മൂല്യം).hexdigest()}
    명령열.append('}')
    for തിരഞ്ഞു_നോക്കൽ_സൂചിക,భాష in enumerate(('java','c','python')):
        ഫയല്_ലിസ്റ്റ്=[(ഡാറ്റാ_പദവി.name,ഡാറ്റാ_പദവി) for ഡാറ്റാ_പദവി in sorted((원본자료/భాష).iterdir()) if ഡാറ്റാ_പദവി.is_file()]
        if భాష=='java':ഫയല്_ലിസ്റ്റ് += [(ഡാറ്റാ_പദവി.stem+'.class',ക്ലാസ്_പാത/(ഡാറ്റാ_പദവി.stem+'.class')) for ഡാറ്റാ_പദവി in 자바실행]
        명령열 += ['if(భాష==%d){'%തിരഞ്ഞു_നോക്കൽ_സൂചിക,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%భాష]
        for പേരു്,വഴി in ഫയല്_ലിസ്റ്റ്:
            ഉള്ളടക്കം_മൂല്യം=guest_bytes(വഴി);ലക്_ഷ്യം='/example/'+భాష+'/'+പേരു്
            if len(ഉള്ളടക്കം_മൂല്യം)>16384 or len(ലക്_ഷ്യം.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ലക്_ഷ്യം)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ലക്_ഷ്യം,ensure_ascii=True),ഉള്ളടക്കം_മൂല്യം.hex()))
            ബണ്ടിൽ_ആവിഷ്കാരം[ലക്_ഷ്യം]={'bytes':len(ഉള്ളടക്കം_മൂല്യം),'sha256':hashlib.sha256(ഉള്ളടക്കം_മൂല്യം).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (വർഗ്ഗമൂലം_പാത/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (അളവ്_ഡാറ്റാ/'manifest.json').write_text(json.dumps(ബണ്ടിൽ_ആവിഷ്കാരം,ensure_ascii=False,indent=2)+'\n')
