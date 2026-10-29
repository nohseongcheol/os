"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(akar_laluan, repositori_laluan, laksanakan_perintah):
    원본자료=repositori_laluan/'example';ukuran_data=akar_laluan/'build/examples';ukuran_data.mkdir(parents=True,exist_ok=True)
    Kelas_laluan=ukuran_data/'classes';Kelas_laluan.mkdir(exist_ok=True)
    자바라이브러리만들기(akar_laluan,laksanakan_perintah)
    ip_settings = read_config(akar_laluan)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = ukuran_data/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    laksanakan_perintah(['javac','--release','8','-encoding','UTF-8','-cp',akar_laluan/'build/java-library/classes','-d',Kelas_laluan]+자바실행)
    suruhan_jujukan=['public final class 예제꾸러미 { public static int pasang_VALUE(int Bahasa) { int 처리값;',
          '처리값=pentafsir_perintah.예제폴더("/example"); if(처리값<0)return 처리값;']
    pakej_manifes_aplikasi={}
    README=guest_bytes(원본자료/'README.md')
    if len(README)>16384: raise ValueError('example README exceeds native VFS limit')
    suruhan_jujukan.append('처리값=pentafsir_perintah.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%README.hex())
    pakej_manifes_aplikasi['/example/README.md']={'bytes':len(README),'sha256':hashlib.sha256(README).hexdigest()}
    suruhan_jujukan.append('if(Bahasa==0){처리값=pentafsir_perintah.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for LALUAN in [원본자료/'python/Melayu.py'] + sorted((akar_laluan/'PYTHON_penghubung/pustaka').glob('*.py')):
        Kandungan_VALUE=guest_bytes(LALUAN);sasaran='/lib/'+LALUAN.name
        if len(Kandungan_VALUE)>16384: raise ValueError('Python library exceeds native VFS limit: '+sasaran)
        suruhan_jujukan.append('처리값=pentafsir_perintah.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(sasaran,ensure_ascii=True),Kandungan_VALUE.hex()))
        pakej_manifes_aplikasi[sasaran]={'bytes':len(Kandungan_VALUE),'sha256':hashlib.sha256(Kandungan_VALUE).hexdigest()}
    suruhan_jujukan.append('}')
    for Carian_INDEX,Bahasa in enumerate(('java','c','python')):
        fail_Senarai=[(data_jawatan.name,data_jawatan) for data_jawatan in sorted((원본자료/Bahasa).iterdir()) if data_jawatan.is_file()]
        if Bahasa=='java':fail_Senarai += [(data_jawatan.stem+'.class',Kelas_laluan/(data_jawatan.stem+'.class')) for data_jawatan in 자바실행]
        suruhan_jujukan += ['if(Bahasa==%d){'%Carian_INDEX,'처리값=pentafsir_perintah.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Bahasa]
        for Nama,LALUAN in fail_Senarai:
            Kandungan_VALUE=guest_bytes(LALUAN);sasaran='/example/'+Bahasa+'/'+Nama
            if len(Kandungan_VALUE)>16384 or len(sasaran.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+sasaran)
            suruhan_jujukan.append('처리값=pentafsir_perintah.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(sasaran,ensure_ascii=True),Kandungan_VALUE.hex()))
            pakej_manifes_aplikasi[sasaran]={'bytes':len(Kandungan_VALUE),'sha256':hashlib.sha256(Kandungan_VALUE).hexdigest()}
        suruhan_jujukan += ['return 0;}']
    suruhan_jujukan += ['return -22;}}']
    (akar_laluan/'build/예제꾸러미.java').write_text('\n'.join(suruhan_jujukan)+'\n')
    (ukuran_data/'manifest.json').write_text(json.dumps(pakej_manifes_aplikasi,ensure_ascii=False,indent=2)+'\n')
