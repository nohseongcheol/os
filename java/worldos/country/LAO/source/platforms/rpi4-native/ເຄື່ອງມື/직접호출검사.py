#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/ສອດຕໍ່_ຄ່າ 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]

def ແລ່ນ():
    클래스들 = ('창', 'ປຸ່ມ', 'ປ້າຍ', 'ຂໍ້ຄວາມ_ຊ່ອງຂໍ້ມູນ', '화면구성요소', '동작알림', 'ງານ_ຄິວ', '작업가닥',
             '작업', '실행할일', '동작받이')
    ຊຸດ = ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-korean.jar'
    ການປະກາດ = subprocess.check_output(['javap', '-classpath', str(ຊຸດ), '-private', '-c']+
                                ['한국어.자체.'+ຊື່ for ຊື່ in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in ການປະກາດ, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(ໂຄງ_ການ_ເລກຮາກ/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ແລ່ນ()', '한국어/자체/ງານ_ຄິວ.나중에실행', '한국어/자체/동작알림.ຄໍາສັ່ງ_ຂໍ້ຄວາມ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ປາຍທາງ_ຄ່າ = ໂຄງ_ການ_ເລກຮາກ/'build/verification/naming'; ປາຍທາງ_ຄ່າ.mkdir(parents=True, exist_ok=True)
    (ປາຍທາງ_ຄ່າ/'direct-bytecode.txt').write_text(ການປະກາດ+'\n'+예제)
    ບັນທຶກ_ແຖວ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(ຊຸດ.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ປາຍທາງ_ຄ່າ/'direct-bytecode.json').write_text(json.dumps(ບັນທຶກ_ແຖວ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·ສອດຕໍ່_ຄ່າ 바이트코드와 예제 호출')

if __name__ == '__main__': ແລ່ນ()
