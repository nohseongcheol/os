"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(ເລກຮາກ_ທາງໂຄຈອນ, ຣີໂພຊິທໍຣີ_ທາງໂຄຈອນ, ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ):
    원본자료=ຣີໂພຊິທໍຣີ_ທາງໂຄຈອນ/'example';ມາດຕະການ_ຂໍ້ມູນ=ເລກຮາກ_ທາງໂຄຈອນ/'build/examples';ມາດຕະການ_ຂໍ້ມູນ.mkdir(parents=True,exist_ok=True)
    ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ=ມາດຕະການ_ຂໍ້ມູນ/'classes';ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ.mkdir(exist_ok=True)
    자바라이브러리만들기(ເລກຮາກ_ທາງໂຄຈອນ,ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ)
    ip_settings = read_config(ເລກຮາກ_ທາງໂຄຈອນ)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = ມາດຕະການ_ຂໍ້ມູນ/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(['javac','--release','8','-encoding','UTF-8','-cp',ເລກຮາກ_ທາງໂຄຈອນ/'build/java-library/classes','-d',ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ]+자바실행)
    명령열=['public final class 예제꾸러미 { public static int ຕິດຕັ້ງ_ຄ່າ(int ພາ_ສາ) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    ຂໍ້ແນະນໍາການໃຊ້=guest_bytes(원본자료/'README.md')
    if len(ຂໍ້ແນະນໍາການໃຊ້)>16384: raise ValueError('example README exceeds native VFS limit')
    명령열.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%ຂໍ້ແນະນໍາການໃຊ້.hex())
    꾸러미명세['/example/README.md']={'bytes':len(ຂໍ້ແນະນໍາການໃຊ້),'sha256':hashlib.sha256(ຂໍ້ແນະນໍາການໃຊ້).hexdigest()}
    명령열.append('if(ພາ_ສາ==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for ທາງໂຄຈອນ in [원본자료/'python/한국어.py'] + sorted((ເລກຮາກ_ທາງໂຄຈອນ/'파이썬연결/ຫໍສະຫມຸດ').glob('*.py')):
        ເນື້ອໃນ_ຄ່າ_cb0f2404=guest_bytes(ທາງໂຄຈອນ);ເປົ້າ_ຫມາຍ='/lib/'+ທາງໂຄຈອນ.name
        if len(ເນື້ອໃນ_ຄ່າ_cb0f2404)>16384 or len(ເປົ້າ_ຫມາຍ.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+ເປົ້າ_ຫມາຍ)
        명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ເປົ້າ_ຫມາຍ,ensure_ascii=True),ເນື້ອໃນ_ຄ່າ_cb0f2404.hex()))
        꾸러미명세[ເປົ້າ_ຫມາຍ]={'bytes':len(ເນື້ອໃນ_ຄ່າ_cb0f2404),'sha256':hashlib.sha256(ເນື້ອໃນ_ຄ່າ_cb0f2404).hexdigest()}
    명령열.append('}')
    for ຄົ້ນຫາ_ດັດຊະນີ,ພາ_ສາ in enumerate(('java','c','python')):
        ຟາຍ_ລາຍຊື່=[(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.name,ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ) for ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ in sorted((원본자료/ພາ_ສາ).iterdir()) if ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.is_file()]
        if ພາ_ສາ=='java':ຟາຍ_ລາຍຊື່ += [(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stem+'.class',ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ/(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.stem+'.class')) for ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ in 자바실행]
        명령열 += ['if(ພາ_ສາ==%d){'%ຄົ້ນຫາ_ດັດຊະນີ,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%ພາ_ສາ]
        for ຊື່,ທາງໂຄຈອນ in ຟາຍ_ລາຍຊື່:
            ເນື້ອໃນ_ຄ່າ_cb0f2404=guest_bytes(ທາງໂຄຈອນ);ເປົ້າ_ຫມາຍ='/example/'+ພາ_ສາ+'/'+ຊື່
            if len(ເນື້ອໃນ_ຄ່າ_cb0f2404)>16384 or len(ເປົ້າ_ຫມາຍ.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ເປົ້າ_ຫມາຍ)
            명령열.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ເປົ້າ_ຫມາຍ,ensure_ascii=True),ເນື້ອໃນ_ຄ່າ_cb0f2404.hex()))
            꾸러미명세[ເປົ້າ_ຫມາຍ]={'bytes':len(ເນື້ອໃນ_ຄ່າ_cb0f2404),'sha256':hashlib.sha256(ເນື້ອໃນ_ຄ່າ_cb0f2404).hexdigest()}
        명령열 += ['return 0;}']
    명령열 += ['return -22;}}']
    (ເລກຮາກ_ທາງໂຄຈອນ/'build/예제꾸러미.java').write_text('\n'.join(명령열)+'\n')
    (ມາດຕະການ_ຂໍ້ມູນ/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
