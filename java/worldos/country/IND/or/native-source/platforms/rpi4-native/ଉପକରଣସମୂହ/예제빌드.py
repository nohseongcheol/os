"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(ରୁଟ୍_ପଥ, 저장소경로, ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ):
    원본자료=저장소경로/'example';ମାପ_ଡାଟା=ରୁଟ୍_ପଥ/'build/examples';ମାପ_ଡାଟା.mkdir(parents=True,exist_ok=True)
    ଶ୍ରେଣୀ_ପଥ=ମାପ_ଡାଟା/'classes';ଶ୍ରେଣୀ_ପଥ.mkdir(exist_ok=True)
    자바라이브러리만들기(ରୁଟ୍_ପଥ,ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ)
    ip_settings = read_config(ରୁଟ୍_ପଥ)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = ମାପ_ଡାଟା/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(['javac','--release','8','-encoding','UTF-8','-cp',ରୁଟ୍_ପଥ/'build/java-library/classes','-d',ଶ୍ରେଣୀ_ପଥ]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int ସଂସ୍ଥାପନ_ମୂଲ୍ୟ(int ଭାଷା) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    ମତେପଢନ୍ତୁ=guest_bytes(원본자료/'README.md')
    if len(ମତେପଢନ୍ତୁ)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%ମତେପଢନ୍ତୁ.hex())
    꾸러미명세['/example/README.md']={'bytes':len(ମତେପଢନ୍ତୁ),'sha256':hashlib.sha256(ମତେପଢନ୍ତୁ).hexdigest()}
    명령열.append('if(ଭାଷା==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ପଥ in [원본자료/'python/한국어.py'] + sorted((ରୁଟ୍_ପଥ/'파이썬연결/ଲାଇବ୍ରେରୀ').glob('*.py')):
        ବିଷୟ_ମୂଲ୍ୟ=guest_bytes(ପଥ);ଲକ୍ଷ୍ୟସ୍ଥଳ='/lib/'+ପଥ.name
        if len(ବିଷୟ_ମୂଲ୍ୟ)>16384: raise ValueError('Python library exceeds native VFS limit: '+ଲକ୍ଷ୍ୟସ୍ଥଳ)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ଲକ୍ଷ୍ୟସ୍ଥଳ,ensure_ascii=True),ବିଷୟ_ମୂଲ୍ୟ.hex()))
        꾸러미명세[ଲକ୍ଷ୍ୟସ୍ଥଳ]={'bytes':len(ବିଷୟ_ମୂଲ୍ୟ),'sha256':hashlib.sha256(ବିଷୟ_ମୂଲ୍ୟ).hexdigest()}
    명령열.append('}')
    for ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା,ଭାଷା in enumerate(('java','c','python')):
        ଫାଇଲ୍_ତାଲିକା=[(ଡାଟା_ସ୍ଥିତି.name,ଡାଟା_ସ୍ଥିତି) for ଡାଟା_ସ୍ଥିତି in sorted((원본자료/ଭାଷା).iterdir()) if ଡାଟା_ସ୍ଥିତି.is_file()]
        if ଭାଷା=='java':ଫାଇଲ୍_ତାଲିକା += [(ଡାଟା_ସ୍ଥିତି.stem+'.class',ଶ୍ରେଣୀ_ପଥ/(ଡାଟା_ସ୍ଥିତି.stem+'.class')) for ଡାଟା_ସ୍ଥିତି in 자바실행]
        명령열 += ['if(ଭାଷା==%d){'%ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%ଭାଷା]
        for ନାମ,ପଥ in ଫାଇଲ୍_ତାଲିକା:
            ବିଷୟ_ମୂଲ୍ୟ=guest_bytes(ପଥ);ଲକ୍ଷ୍ୟସ୍ଥଳ='/example/'+ଭାଷା+'/'+ନାମ
            if len(ବିଷୟ_ମୂଲ୍ୟ)>16384 or len(ଲକ୍ଷ୍ୟସ୍ଥଳ.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ଲକ୍ଷ୍ୟସ୍ଥଳ)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ଲକ୍ଷ୍ୟସ୍ଥଳ,ensure_ascii=True),ବିଷୟ_ମୂଲ୍ୟ.hex()))
            꾸러미명세[ଲକ୍ଷ୍ୟସ୍ଥଳ]={'bytes':len(ବିଷୟ_ମୂଲ୍ୟ),'sha256':hashlib.sha256(ବିଷୟ_ମୂଲ୍ୟ).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (ରୁଟ୍_ପଥ/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (ମାପ_ଡାଟା/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
