"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, 실행):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    akotchijuushi_wopu_a_ttaaleemüin=결과자료/'classes';akotchijuushi_wopu_a_ttaaleemüin.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,실행)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    실행(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',akotchijuushi_wopu_a_ttaaleemüin]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int e_itawaa_ajutuu(int anüikii_komputatooralujatü) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    PAASHAJE_ERAN=guest_bytes(원본자료/'README.md')
    if len(PAASHAJE_ERAN)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%PAASHAJE_ERAN.hex())
    꾸러미명세['/example/README.md']={'bytes':len(PAASHAJE_ERAN),'sha256':hashlib.sha256(PAASHAJE_ERAN).hexdigest()}
    명령열.append('if(anüikii_komputatooralujatü==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for wopu_a_ttaaleemüin in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/anaajaalee').glob('*.py')):
        alu_ujatüü_ajutuu=guest_bytes(wopu_a_ttaaleemüin);대상='/lib/'+wopu_a_ttaaleemüin.name
        if len(alu_ujatüü_ajutuu)>16384: raise ValueError('Python library exceeds native VFS limit: '+대상)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(대상,ensure_ascii=True),alu_ujatüü_ajutuu.hex()))
        꾸러미명세[대상]={'bytes':len(alu_ujatüü_ajutuu),'sha256':hashlib.sha256(alu_ujatüü_ajutuu).hexdigest()}
    명령열.append('}')
    for 색인,anüikii_komputatooralujatü in enumerate(('java','c','python')):
        파일목록=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/anüikii_komputatooralujatü).iterdir()) if 자료위치.is_file()]
        if anüikii_komputatooralujatü=='java':파일목록 += [(자료위치.stem+'.class',akotchijuushi_wopu_a_ttaaleemüin/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        명령열 += ['if(anüikii_komputatooralujatü==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%anüikii_komputatooralujatü]
        for 이름,wopu_a_ttaaleemüin in 파일목록:
            alu_ujatüü_ajutuu=guest_bytes(wopu_a_ttaaleemüin);대상='/example/'+anüikii_komputatooralujatü+'/'+이름
            if len(alu_ujatüü_ajutuu)>16384 or len(대상.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+대상)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(대상,ensure_ascii=True),alu_ujatüü_ajutuu.hex()))
            꾸러미명세[대상]={'bytes':len(alu_ujatüü_ajutuu),'sha256':hashlib.sha256(alu_ujatüü_ajutuu).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
