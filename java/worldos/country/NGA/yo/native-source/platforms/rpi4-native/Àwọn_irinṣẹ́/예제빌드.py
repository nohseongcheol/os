"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, ṣiṣẹ́_àṣẹ):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    ọ̀wọ́_ọ̀nà=결과자료/'classes';ọ̀wọ́_ọ̀nà.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,ṣiṣẹ́_àṣẹ)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ṣiṣẹ́_àṣẹ(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',ọ̀wọ́_ọ̀nà]+자바실행)
    ìtọ́sọ́nà_ÀTẸ̀LÉRA=['public final class 예제꾸러미 { public static int ṣàgbékalẹ̀_iye(int Èdè) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    KÀ_MÍ=guest_bytes(원본자료/'README.md')
    if len(KÀ_MÍ)>16384: raise ValueError('example README exceeds native VFS limit')
    ìtọ́sọ́nà_ÀTẸ̀LÉRA.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%KÀ_MÍ.hex())
    꾸러미명세['/example/README.md']={'bytes':len(KÀ_MÍ),'sha256':hashlib.sha256(KÀ_MÍ).hexdigest()}
    ìtọ́sọ́nà_ÀTẸ̀LÉRA.append('if(Èdè==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ọ̀nà in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/ibi_ìpamọ́').glob('*.py')):
        Àkóónú_iye=guest_bytes(ọ̀nà);àfojúsùn='/lib/'+ọ̀nà.name
        if len(Àkóónú_iye)>16384: raise ValueError('Python library exceeds native VFS limit: '+àfojúsùn)
        ìtọ́sọ́nà_ÀTẸ̀LÉRA.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(àfojúsùn,ensure_ascii=True),Àkóónú_iye.hex()))
        꾸러미명세[àfojúsùn]={'bytes':len(Àkóónú_iye),'sha256':hashlib.sha256(Àkóónú_iye).hexdigest()}
    ìtọ́sọ́nà_ÀTẸ̀LÉRA.append('}')
    for 색인,Èdè in enumerate(('java','c','python')):
        fáìlì_Àtòkọ=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/Èdè).iterdir()) if 자료위치.is_file()]
        if Èdè=='java':fáìlì_Àtòkọ += [(자료위치.stem+'.class',ọ̀wọ́_ọ̀nà/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        ìtọ́sọ́nà_ÀTẸ̀LÉRA += ['if(Èdè==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Èdè]
        for Orúkọ,ọ̀nà in fáìlì_Àtòkọ:
            Àkóónú_iye=guest_bytes(ọ̀nà);àfojúsùn='/example/'+Èdè+'/'+Orúkọ
            if len(Àkóónú_iye)>16384 or len(àfojúsùn.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+àfojúsùn)
            ìtọ́sọ́nà_ÀTẸ̀LÉRA.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(àfojúsùn,ensure_ascii=True),Àkóónú_iye.hex()))
            꾸러미명세[àfojúsùn]={'bytes':len(Àkóónú_iye),'sha256':hashlib.sha256(Àkóónú_iye).hexdigest()}
        ìtọ́sọ́nà_ÀTẸ̀LÉRA += ['return 0;}']
    ìtọ́sọ́nà_ÀTẸ̀LÉRA += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(ìtọ́sọ́nà_ÀTẸ̀LÉRA)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
