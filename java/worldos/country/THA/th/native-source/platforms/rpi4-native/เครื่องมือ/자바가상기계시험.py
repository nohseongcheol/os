#!/usr/bin/env python3
"""OpenJDK와 เอง ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ดําเนินการ_คําสั่ง import แสดง_ราก


def เรียกใช้งาน():
    ผลผลิต = แสดง_ราก / 'build/verification/jvm'
    คลาส_พาธ = ผลผลิต / 'classes'; คลาส_พาธ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = แสดง_ราก / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((แสดง_ราก / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(คลาส_พาธ)] + [str(สตริง_ข้อมูล) for สตริง_ข้อมูล in 원문목록])
    รายการทดสอบ = [('객체시험', ['พื้นหลัง_ค่า', 'สาขา_ค่า', '계산가능']), ('예외시험', []), ('ประชากร_การทดสอบ', []),
             ('가닥시험', ['ตัวนับ_ค่า', 'งาน_แอคชัน', 'เธรด_ค่า']), ('한글시험', []), ('การทดสอบ_ระบบเครือข่าย', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ตรวจสอบความถูกต้อง.การทดสอบ_รวม', []), ('진입호환시험', [])]
    การตรวจสอบความถูกต้อง_รายงาน = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((แสดง_ราก / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ชื่อ, 포함인수 in รายการทดสอบ:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(คลาส_พาธ) + ':' + str(자바꾸러미), ชื่อ], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(แสดง_ราก / 'เครื่องมือ/ดําเนินการ_แฟ้ม.py'), str(คลาส_พาธ / (ชื่อ.replace('.', '/') + '.class'))]
            if '.' in ชื่อ: 명령인수 += ['--class-name', ชื่อ]
            for รวม_e6c90571 in 포함인수: 명령인수 += ['--include', str(คลาส_พาธ / (รวม_e6c90571 + '.class'))]
            if ชื่อ == '한글소스': 명령인수[2] = str(แสดง_ราก / '시험/자바/한글소스.java')
            เสร็จสมบูรณ์_จํานวน = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ค่าจริง_เมตริก = เสร็จสมบูรณ์_จํานวน.stdout.decode('utf-8').replace('\r\n', '\n')
            (ผลผลิต / (ชื่อ + '.log')).write_text(ค่าจริง_เมตริก, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", ค่าจริง_เมตริก, re.S)
            assert เสร็จสมบูรณ์_จํานวน.returncode == 0 and 일치, (ชื่อ, ค่าจริง_เมตริก)
            ผลลัพธ์ = next(สตริง_ข้อมูล for สตริง_ข้อมูล in 일치.groups() if สตริง_ข้อมูล is not None) + '\n'
            assert ผลลัพธ์ == 예상결과, (ชื่อ, 예상결과, ผลลัพธ์)
            การตรวจสอบความถูกต้อง_รายงาน['tests'].append({'name': ชื่อ, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ชื่อ, flush=True)
        # เอง JVM에 직접 연결한 ไทย เธรด_ค่า/진입점은 OpenJDK용 래퍼가 아니다.
        เสร็จสมบูรณ์_จํานวน = subprocess.run(['python3', str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_แฟ้ม.py'), str(คลาส_พาธ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ผลลัพธ์ = เสร็จสมบูรณ์_จํานวน.stdout.decode('utf-8').replace('\r\n', '\n')
        (ผลผลิต/'한국어가닥시험.log').write_text(ผลลัพธ์)
        assert เสร็จสมบูรณ์_จํานวน.returncode == 0 and 'ไทย 직접 เธรด_ค่า ส่งต่อ_ค่า\n' in ผลลัพธ์ and '\nexit 0\n' in ผลลัพธ์, ผลลัพธ์
        การตรวจสอบความถูกต้อง_รายงาน['direct_korean_thread_and_entry'] = True
        print('PASS: ไทย 직접 เธรด_ค่า·เรียกทํางาน·เรียกใช้งาน จุดเข้าใช้งาน', flush=True)
        ถูกต้อง = (คลาส_พาธ / '객체시험.class').read_bytes()
        กรณีทดสอบ = [('판거부', ถูกต้อง[:6] + b'\x00\x35' + ถูกต้อง[8:], 'supported class versions'),
                 ('잘린클래스', ถูกต้อง[:24], 'truncated class file')]
        การตรวจสอบความถูกต้อง_รายงาน['rejection_tests'] = []
        for ชื่อ, ส่วนข้อมูล_ข้อมูล, ข้อสังเกต_ข้อความ in กรณีทดสอบ:
            การทดสอบ_ข้อมูล = ผลผลิต / (ชื่อ + '.class'); การทดสอบ_ข้อมูล.write_bytes(ส่วนข้อมูล_ข้อมูล)
            เสร็จสมบูรณ์_จํานวน = subprocess.run(['python3', str(แสดง_ราก / 'เครื่องมือ/ดําเนินการ_แฟ้ม.py'), str(การทดสอบ_ข้อมูล)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ข้อความ = เสร็จสมบูรณ์_จํานวน.stdout.decode('utf-8').replace('\r\n', '\n')
            (ผลผลิต / (ชื่อ + '.log')).write_text(ข้อความ, encoding='utf-8')
            assert เสร็จสมบูรณ์_จํานวน.returncode == 1 and ข้อสังเกต_ข้อความ in ข้อความ and 'exit 1\n' in ข้อความ, (ชื่อ, ข้อความ)
            การตรวจสอบความถูกต้อง_รายงาน['rejection_tests'].append({'name': ชื่อ, 'passed': True})
            print('PASS (rejected):', ชื่อ, flush=True)
        การตรวจสอบความถูกต้อง_รายงาน['passed'] = True
    finally:
        (ผลผลิต / 'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    เรียกใช้งาน()
