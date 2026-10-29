"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(akar_jalur, repositori_jalur, Jalankan_perintah):
    원본자료=repositori_jalur/'example';KR_data=akar_jalur/'build/examples';KR_data.mkdir(parents=True,exist_ok=True)
    Kelas_jalur=KR_data/'classes';Kelas_jalur.mkdir(exist_ok=True)
    자바라이브러리만들기(akar_jalur,Jalankan_perintah)
    ip_settings = read_config(akar_jalur)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = KR_data/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    Jalankan_perintah(['javac','--release','8','-encoding','UTF-8','-cp',akar_jalur/'build/java-library/classes','-d',Kelas_jalur]+자바실행)
    instruksi_urutan=['public final class 예제꾸러미 { public static int instal_VALUE(int Bahasa) { int 처리값;',
          '처리값=PenafsirPerintah.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    baca_saya=guest_bytes(원본자료/'README.md')
    if len(baca_saya)>16384: raise ValueError('example README exceeds native VFS limit')
    instruksi_urutan.append('처리값=PenafsirPerintah.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%baca_saya.hex())
    꾸러미명세['/example/README.md']={'bytes':len(baca_saya),'sha256':hashlib.sha256(baca_saya).hexdigest()}
    instruksi_urutan.append('if(Bahasa==0){처리값=PenafsirPerintah.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for jalur in [원본자료/'python/Indonesia.py'] + sorted((akar_jalur/'PYTHON_bridge/pustaka').glob('*.py')):
        Isi_VALUE=guest_bytes(jalur);target='/lib/'+jalur.name
        if len(Isi_VALUE)>16384: raise ValueError('Python library exceeds native VFS limit: '+target)
        instruksi_urutan.append('처리값=PenafsirPerintah.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(target,ensure_ascii=True),Isi_VALUE.hex()))
        꾸러미명세[target]={'bytes':len(Isi_VALUE),'sha256':hashlib.sha256(Isi_VALUE).hexdigest()}
    instruksi_urutan.append('}')
    for LOOKUP_INDEX,Bahasa in enumerate(('java','c','python')):
        file_Daftar=[(data_posisi.name,data_posisi) for data_posisi in sorted((원본자료/Bahasa).iterdir()) if data_posisi.is_file()]
        if Bahasa=='java':file_Daftar += [(data_posisi.stem+'.class',Kelas_jalur/(data_posisi.stem+'.class')) for data_posisi in 자바실행]
        instruksi_urutan += ['if(Bahasa==%d){'%LOOKUP_INDEX,'처리값=PenafsirPerintah.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%Bahasa]
        for Nama_2,jalur in file_Daftar:
            Isi_VALUE=guest_bytes(jalur);target='/example/'+Bahasa+'/'+Nama_2
            if len(Isi_VALUE)>16384 or len(target.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+target)
            instruksi_urutan.append('처리값=PenafsirPerintah.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(target,ensure_ascii=True),Isi_VALUE.hex()))
            꾸러미명세[target]={'bytes':len(Isi_VALUE),'sha256':hashlib.sha256(Isi_VALUE).hexdigest()}
        instruksi_urutan += ['return 0;}']
    instruksi_urutan += ['return -22;}}']
    (akar_jalur/'build/예제꾸러미.java').write_text('\n'.join(instruksi_urutan)+'\n')
    (KR_data/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
