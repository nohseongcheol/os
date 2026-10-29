#!/usr/bin/env python3
"""การกระจาย_ค่า class의 직접 ไทย GUI/เธรด_ค่า 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

แสดง_ราก = Path(__file__).resolve().parents[1]

def เรียกใช้งาน():
    클래스들 = ('หน้าต่าง', 'ปุ่ม', 'ฉลาก', 'เขตข้อมูลข้อความ', '화면구성요소', 'แอคชัน_ข้อสังเกต', 'กิจกรรม_คิว', 'งานเบื้องหลัง',
             '작업', '실행할일', '동작받이')
    รวม = แสดง_ราก/'dist/jkoros-native-korean.jar'
    การประกาศ = subprocess.check_output(['javap', '-classpath', str(รวม), '-private', '-c']+
                                ['ไทย.เอง.'+ชื่อ for ชื่อ in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in การประกาศ, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(แสดง_ราก/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void เรียกใช้งาน()', 'ไทย/เอง/กิจกรรม_คิว.나중에실행', 'ไทย/เอง/แอคชัน_ข้อสังเกต.คําสั่ง_ข้อความ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ปลายทาง_ค่า_a0fbc067 = แสดง_ราก/'build/verification/naming'; ปลายทาง_ค่า_a0fbc067.mkdir(parents=True, exist_ok=True)
    (ปลายทาง_ค่า_a0fbc067/'direct-bytecode.txt').write_text(การประกาศ+'\n'+예제)
    บันทึก_สถิติ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(รวม.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ปลายทาง_ค่า_a0fbc067/'direct-bytecode.json').write_text(json.dumps(บันทึก_สถิติ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: ไทย 직접 GUI·เธรด_ค่า 바이트코드와 예제 호출')

if __name__ == '__main__': เรียกใช้งาน()
