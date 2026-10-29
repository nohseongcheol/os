"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(ราก_พาธ, ที่เก็บ_พาธ, ดําเนินการ_คําสั่ง):
    원본자료=ที่เก็บ_พาธ/'example';เมตริก_ข้อมูล=ราก_พาธ/'build/examples';เมตริก_ข้อมูล.mkdir(parents=True,exist_ok=True)
    คลาส_พาธ=เมตริก_ข้อมูล/'classes';คลาส_พาธ.mkdir(exist_ok=True)
    자바라이브러리만들기(ราก_พาธ,ดําเนินการ_คําสั่ง)
    ip_settings = read_config(ราก_พาธ)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = เมตริก_ข้อมูล/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ดําเนินการ_คําสั่ง(['javac','--release','8','-encoding','UTF-8','-cp',ราก_พาธ/'build/java-library/classes','-d',คลาส_พาธ]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int ติดตั้ง_ค่า(int ภาษา) { int 처리값;',
          '처리값=ตัวแปลคําสั่ง.예제폴더("/example"); if(처리값<0)return 처리값;']
    รวม_ไฟล์กํากับ={}
    안내자료=guest_bytes(원본자료/'README.md')
    if len(안내자료)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=ตัวแปลคําสั่ง.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%안내자료.hex())
    รวม_ไฟล์กํากับ['/example/README.md']={'bytes':len(안내자료),'sha256':hashlib.sha256(안내자료).hexdigest()}
    명령열.append('if(ภาษา==0){처리값=ตัวแปลคําสั่ง.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for เส้นทาง in [원본자료/'python/ไทย.py'] + sorted((ราก_พาธ/'파이썬연결/ไลบรารี').glob('*.py')):
        เนื้อหา_ค่า=guest_bytes(เส้นทาง);เป้าหมาย='/lib/'+เส้นทาง.name
        if len(เนื้อหา_ค่า)>16384: raise ValueError('Python library exceeds native VFS limit: '+เป้าหมาย)
        명령열.append('처리값=ตัวแปลคําสั่ง.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(เป้าหมาย,ensure_ascii=True),เนื้อหา_ค่า.hex()))
        รวม_ไฟล์กํากับ[เป้าหมาย]={'bytes':len(เนื้อหา_ค่า),'sha256':hashlib.sha256(เนื้อหา_ค่า).hexdigest()}
    명령열.append('}')
    for การค้นหา_ดัชนี,ภาษา in enumerate(('java','c','python')):
        แฟ้ม_รายการ=[(ข้อมูล_ตําแหน่ง.name,ข้อมูล_ตําแหน่ง) for ข้อมูล_ตําแหน่ง in sorted((원본자료/ภาษา).iterdir()) if ข้อมูล_ตําแหน่ง.is_file()]
        if ภาษา=='java':แฟ้ม_รายการ += [(ข้อมูล_ตําแหน่ง.stem+'.class',คลาส_พาธ/(ข้อมูล_ตําแหน่ง.stem+'.class')) for ข้อมูล_ตําแหน่ง in 자바실행]
        명령열 += ['if(ภาษา==%d){'%การค้นหา_ดัชนี,'처리값=ตัวแปลคําสั่ง.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%ภาษา]
        for ชื่อ,เส้นทาง in แฟ้ม_รายการ:
            เนื้อหา_ค่า=guest_bytes(เส้นทาง);เป้าหมาย='/example/'+ภาษา+'/'+ชื่อ
            if len(เนื้อหา_ค่า)>16384 or len(เป้าหมาย.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+เป้าหมาย)
            명령열.append('처리값=ตัวแปลคําสั่ง.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(เป้าหมาย,ensure_ascii=True),เนื้อหา_ค่า.hex()))
            รวม_ไฟล์กํากับ[เป้าหมาย]={'bytes':len(เนื้อหา_ค่า),'sha256':hashlib.sha256(เนื้อหา_ค่า).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (ราก_พาธ/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (เมตริก_ข้อมูล/'manifest.json').write_text(json.dumps(รวม_ไฟล์กํากับ,ensure_ascii=False,indent=2)+'\n')
