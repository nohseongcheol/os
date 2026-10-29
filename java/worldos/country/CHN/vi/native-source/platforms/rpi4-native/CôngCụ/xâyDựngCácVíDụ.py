"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from xâyDựngThưViệnJava import tạoThưViệnJava


def tạoCácVíDụ(đườngDẫnGốcCây, đườngDẫnKhoNguồn, thựcThiLệnh):
    dữLiệuNguyênBản=đườngDẫnKhoNguồn/'example';dữLiệuKếtQuả=đườngDẫnGốcCây/'build/examples';dữLiệuKếtQuả.mkdir(parents=True,exist_ok=True)
    đườngDẫnLớp=dữLiệuKếtQuả/'classes';đườngDẫnLớp.mkdir(exist_ok=True)
    tạoThưViệnJava(đườngDẫnGốcCây,thựcThiLệnh)
    ip_settings = read_config(đườngDẫnGốcCây)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = dữLiệuKếtQuả/'java-source'; java_sources.mkdir(exist_ok=True)
    thựcThiJava=[]
    for path in sorted((dữLiệuNguyênBản/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); thựcThiJava.append(target)
    thựcThiLệnh(['javac','--release','8','-encoding','UTF-8','-cp',đườngDẫnGốcCây/'build/java-library/classes','-d',đườngDẫnLớp]+thựcThiJava)
    dãyChỉLệnh=['public final class GóiGộpVíDụ { public static int càiĐặtGiáTrị(int NgônNgữ) { int giáTrịĐãXửLý;',
          'giáTrịĐãXửLý=TrìnhThôngDịchLệnh.thưMụcVíDụ("/example"); if(giáTrịĐãXửLý<0)return giáTrịĐãXửLý;']
    bảnKêGóiGộp={}
    hãyĐọc=guest_bytes(dữLiệuNguyênBản/'README.md')
    if len(hãyĐọc)>16384: raise ValueError('example README exceeds native VFS limit')
    dãyChỉLệnh.append('giáTrịĐãXửLý=TrìnhThôngDịchLệnh.tệpVíDụ("/example/README.md","%s"); if(giáTrịĐãXửLý<0)return giáTrịĐãXửLý;'%hãyĐọc.hex())
    bảnKêGóiGộp['/example/README.md']={'bytes':len(hãyĐọc),'sha256':hashlib.sha256(hãyĐọc).hexdigest()}
    dãyChỉLệnh.append('if(NgônNgữ==0){giáTrịĐãXửLý=TrìnhThôngDịchLệnh.thưMụcVíDụ("/lib"); if(giáTrịĐãXửLý<0)return giáTrịĐãXửLý;')
    for đườngDẫn in [dữLiệuNguyênBản/'python/tiếngViệt.py'] + sorted((đườngDẫnGốcCây/'cầuNốiPython/thưViện').glob('*.py')):
        giáTrịNộiDung=guest_bytes(đườngDẫn);giáTrịĐốiĐích='/lib/'+đườngDẫn.name
        if len(giáTrịNộiDung)>16384 or len(giáTrịĐốiĐích.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+giáTrịĐốiĐích)
        dãyChỉLệnh.append('giáTrịĐãXửLý=TrìnhThôngDịchLệnh.tệpVíDụ(%s,"%s"); if(giáTrịĐãXửLý<0)return giáTrịĐãXửLý;'%(json.dumps(giáTrịĐốiĐích,ensure_ascii=True),giáTrịNộiDung.hex()))
        bảnKêGóiGộp[giáTrịĐốiĐích]={'bytes':len(giáTrịNộiDung),'sha256':hashlib.sha256(giáTrịNộiDung).hexdigest()}
    dãyChỉLệnh.append('}')
    for chỉSốTraCứu,NgônNgữ in enumerate(('java','c','python')):
        danhSáchTệp=[(vịTríDữLiệu.name,vịTríDữLiệu) for vịTríDữLiệu in sorted((dữLiệuNguyênBản/NgônNgữ).iterdir()) if vịTríDữLiệu.is_file()]
        if NgônNgữ=='java':danhSáchTệp += [(vịTríDữLiệu.stem+'.class',đườngDẫnLớp/(vịTríDữLiệu.stem+'.class')) for vịTríDữLiệu in thựcThiJava]
        dãyChỉLệnh += ['if(NgônNgữ==%d){'%chỉSốTraCứu,'giáTrịĐãXửLý=TrìnhThôngDịchLệnh.thưMụcVíDụ("/example/%s"); if(giáTrịĐãXửLý<0)return giáTrịĐãXửLý;'%NgônNgữ]
        for tên,đườngDẫn in danhSáchTệp:
            giáTrịNộiDung=guest_bytes(đườngDẫn);giáTrịĐốiĐích='/example/'+NgônNgữ+'/'+tên
            if len(giáTrịNộiDung)>16384 or len(giáTrịĐốiĐích.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+giáTrịĐốiĐích)
            dãyChỉLệnh.append('giáTrịĐãXửLý=TrìnhThôngDịchLệnh.tệpVíDụ(%s,"%s"); if(giáTrịĐãXửLý<0)return giáTrịĐãXửLý;'%(json.dumps(giáTrịĐốiĐích,ensure_ascii=True),giáTrịNộiDung.hex()))
            bảnKêGóiGộp[giáTrịĐốiĐích]={'bytes':len(giáTrịNộiDung),'sha256':hashlib.sha256(giáTrịNộiDung).hexdigest()}
        dãyChỉLệnh += ['return 0;}']
    dãyChỉLệnh += ['return -22;}}']
    (đườngDẫnGốcCây/'build/GóiGộpVíDụ.java').write_text('\n'.join(dãyChỉLệnh)+'\n')
    (dữLiệuKếtQuả/'manifest.json').write_text(json.dumps(bảnKêGóiGộp,ensure_ascii=False,indent=2)+'\n')
