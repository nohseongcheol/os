"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(ឬស_ផ្លូវ, ឃ្លាំង_ផ្ទុក_ផ្លូវ, អនុវត្ត_ពាក្យបញ្ជា):
    원본자료=ឃ្លាំង_ផ្ទុក_ផ្លូវ/'example';ការវាស់វែង_ទិន្នន័យ=ឬស_ផ្លូវ/'build/examples';ការវាស់វែង_ទិន្នន័យ.mkdir(parents=True,exist_ok=True)
    ថ្នាក់_ផ្លូវ=ការវាស់វែង_ទិន្នន័យ/'classes';ថ្នាក់_ផ្លូវ.mkdir(exist_ok=True)
    자바라이브러리만들기(ឬស_ផ្លូវ,អនុវត្ត_ពាក្យបញ្ជា)
    ip_settings = read_config(ឬស_ផ្លូវ)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = ការវាស់វែង_ទិន្នន័យ/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    អនុវត្ត_ពាក្យបញ្ជា(['javac','--release','8','-encoding','UTF-8','-cp',ឬស_ផ្លូវ/'build/java-library/classes','-d',ថ្នាក់_ផ្លូវ]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int ដំឡើង_តំលៃ(int ភាសា) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    អានខ្ញុំ=guest_bytes(원본자료/'README.md')
    if len(អានខ្ញុំ)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%អានខ្ញុំ.hex())
    꾸러미명세['/example/README.md']={'bytes':len(អានខ្ញុំ),'sha256':hashlib.sha256(អានខ្ញុំ).hexdigest()}
    명령열.append('if(ភាសា==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ផ្លូវ in [원본자료/'python/한국어.py'] + sorted((ឬស_ផ្លូវ/'파이썬연결/បណ្ណាល័យ').glob('*.py')):
        មាតិកា_តំលៃ=guest_bytes(ផ្លូវ);គោលដៅ='/lib/'+ផ្លូវ.name
        if len(មាតិកា_តំលៃ)>16384: raise ValueError('Python library exceeds native VFS limit: '+គោលដៅ)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(គោលដៅ,ensure_ascii=True),មាតិកា_តំលៃ.hex()))
        꾸러미명세[គោលដៅ]={'bytes':len(មាតិកា_តំលៃ),'sha256':hashlib.sha256(មាតិកា_តំលៃ).hexdigest()}
    명령열.append('}')
    for រុករក_សន្ទស្សន៏,ភាសា in enumerate(('java','c','python')):
        ឯកសារ_បញ្ជី=[(ទិន្នន័យ_កំណត់ទីតាំង.name,ទិន្នន័យ_កំណត់ទីតាំង) for ទិន្នន័យ_កំណត់ទីតាំង in sorted((원본자료/ភាសា).iterdir()) if ទិន្នន័យ_កំណត់ទីតាំង.is_file()]
        if ភាសា=='java':ឯកសារ_បញ្ជី += [(ទិន្នន័យ_កំណត់ទីតាំង.stem+'.class',ថ្នាក់_ផ្លូវ/(ទិន្នន័យ_កំណត់ទីតាំង.stem+'.class')) for ទិន្នន័យ_កំណត់ទីតាំង in 자바실행]
        명령열 += ['if(ភាសា==%d){'%រុករក_សន្ទស្សន៏,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%ភាសា]
        for ឈ្មោះ,ផ្លូវ in ឯកសារ_បញ្ជី:
            មាតិកា_តំលៃ=guest_bytes(ផ្លូវ);គោលដៅ='/example/'+ភាសា+'/'+ឈ្មោះ
            if len(មាតិកា_តំលៃ)>16384 or len(គោលដៅ.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+គោលដៅ)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(គោលដៅ,ensure_ascii=True),មាតិកា_តំលៃ.hex()))
            꾸러미명세[គោលដៅ]={'bytes':len(មាតិកា_តំលៃ),'sha256':hashlib.sha256(មាតិកា_តំលៃ).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (ឬស_ផ្លូវ/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (ការវាស់វែង_ទិន្នន័យ/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
