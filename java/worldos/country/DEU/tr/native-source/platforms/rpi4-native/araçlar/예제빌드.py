"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(kök_yol, depo_yol, yürütmek_komut):
    원본자료=depo_yol/'example';KR_veri=kök_yol/'build/examples';KR_veri.mkdir(parents=True,exist_ok=True)
    Sınıf_yol=KR_veri/'classes';Sınıf_yol.mkdir(exist_ok=True)
    자바라이브러리만들기(kök_yol,yürütmek_komut)
    ip_settings = read_config(kök_yol)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KR_veri/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    yürütmek_komut(['javac','--release','8','-encoding','UTF-8','-cp',kök_yol/'build/java-library/classes','-d',Sınıf_yol]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int yükle_değer(int Dil) { int 처리값;',
          '처리값=KomutYorumlayıcı.예제폴더("/example"); if(처리값<0)return 처리값;']
    paket_iş_bildirim={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=KomutYorumlayıcı.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    paket_iş_bildirim['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    명령열.append('if(Dil==0){처리값=KomutYorumlayıcı.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for yol in [원본자료/'python/Türkçe.py'] + sorted((kök_yol/'PYTHON_köprü/kitaplık').glob('*.py')):
        içerik_değer=guest_bytes(yol);hedef='/lib/'+yol.name
        if len(içerik_değer)>16384: raise ValueError('Python library exceeds native VFS limit: '+hedef)
        명령열.append('처리값=KomutYorumlayıcı.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(hedef,ensure_ascii=True),içerik_değer.hex()))
        paket_iş_bildirim[hedef]={'bytes':len(içerik_değer),'sha256':hashlib.sha256(içerik_değer).hexdigest()}
    명령열.append('}')
    for ARA_Dizin,Dil in enumerate(('java','c','python')):
        dosya_listesi=[(veri_konum.name,veri_konum) for veri_konum in sorted((원본자료/Dil).iterdir()) if veri_konum.is_file()]
        if Dil=='java':dosya_listesi += [(veri_konum.stem+'.class',Sınıf_yol/(veri_konum.stem+'.class')) for veri_konum in 자바실행]
        명령열 += ['if(Dil==%d){'%ARA_Dizin,'처리값=KomutYorumlayıcı.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Dil]
        for İsim,yol in dosya_listesi:
            içerik_değer=guest_bytes(yol);hedef='/example/'+Dil+'/'+İsim
            if len(içerik_değer)>16384 or len(hedef.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+hedef)
            명령열.append('처리값=KomutYorumlayıcı.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(hedef,ensure_ascii=True),içerik_değer.hex()))
            paket_iş_bildirim[hedef]={'bytes':len(içerik_değer),'sha256':hashlib.sha256(içerik_değer).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (kök_yol/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (KR_veri/'manifest.json').write_text(json.dumps(paket_iş_bildirim,ensure_ascii=False,indent=2)+'\n')
