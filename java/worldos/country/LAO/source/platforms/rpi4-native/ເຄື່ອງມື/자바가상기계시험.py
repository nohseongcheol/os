#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ


def ແລ່ນ():
    출력결과 = ໂຄງ_ການ_ເລກຮາກ / 'build/verification/jvm'
    ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ = 출력결과 / 'classes'; ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = ໂຄງ_ການ_ເລກຮາກ / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((ໂຄງ_ການ_ເລກຮາກ / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ)] + [str(ສະຕຣິງ_ຂໍ້ມູນ) for ສະຕຣິງ_ຂໍ້ມູນ in 원문목록])
    시험목록 = [('객체시험', ['ພື້ນຫຼັງ_ຄ່າ', 'ສາຂາ_ຄ່າ', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['ເຄື່ອງ_ນັບ_ຄ່າ', 'ຫນ້າວຽກ_ຄໍາສັ່ງ', 'ສອດຕໍ່_ຄ່າ']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ຮັບ_ຮອງ.꾸러미시험', []), ('진입호환시험', [])]
    ໃຊ້ໄດ້_ລາຍງານ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ຊື່, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ) + ':' + str(자바꾸러미), ຊື່], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຟາຍ.py'), str(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ / (ຊື່.replace('.', '/') + '.class'))]
            if '.' in ຊື່: 명령인수 += ['--class-name', ຊື່]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ / (포함항목 + '.class'))]
            if ຊື່ == '한글소스': 명령인수[2] = str(ໂຄງ_ການ_ເລກຮາກ / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ຕົວ_ຈິງ_ມາດຕະການ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ຊື່ + '.log')).write_text(ຕົວ_ຈິງ_ມາດຕະການ, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", ຕົວ_ຈິງ_ມາດຕະການ, re.S)
            assert 완료량.returncode == 0 and 일치, (ຊື່, ຕົວ_ຈິງ_ມາດຕະການ)
            ມາດຕະການ = next(ສະຕຣິງ_ຂໍ້ມູນ for ສະຕຣິງ_ຂໍ້ມູນ in 일치.groups() if ສະຕຣິງ_ຂໍ້ມູນ is not None) + '\n'
            assert ມາດຕະການ == 예상결과, (ຊື່, 예상결과, ມາດຕະການ)
            ໃຊ້ໄດ້_ລາຍງານ['tests'].append({'name': ຊື່, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ຊື່, flush=True)
        # 자체 JVM에 직접 연결한 한국어 ສອດຕໍ່_ຄ່າ/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຟາຍ.py'), str(ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ມາດຕະການ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(ມາດຕະການ)
        assert 완료량.returncode == 0 and '한국어 직접 ສອດຕໍ່_ຄ່າ ປີ້_ຄ່າ\n' in ມາດຕະການ and '\nexit 0\n' in ມາດຕະການ, ມາດຕະການ
        ໃຊ້ໄດ້_ລາຍງານ['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 ສອດຕໍ່_ຄ່າ·ປະ_ຕິ_ບັດ_ຫນ້າວຽກ·ແລ່ນ ເຂົ້າໃນ_ຈຸດ', flush=True)
        유효함 = (ປະເພດສິ່ງຂອງ_ທາງໂຄຈອນ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        ໃຊ້ໄດ້_ລາຍງານ['rejection_tests'] = []
        for ຊື່, ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ, 알림문 in 시험사례:
            시험자료 = 출력결과 / (ຊື່ + '.class'); 시험자료.write_bytes(ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ)
            완료량 = subprocess.run(['python3', str(ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຟາຍ.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            ຂໍ້ຄວາມ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ຊື່ + '.log')).write_text(ຂໍ້ຄວາມ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in ຂໍ້ຄວາມ and 'exit 1\n' in ຂໍ້ຄວາມ, (ຊື່, ຂໍ້ຄວາມ)
            ໃຊ້ໄດ້_ລາຍງານ['rejection_tests'].append({'name': ຊື່, 'passed': True})
            print('PASS (rejected):', ຊື່, flush=True)
        ໃຊ້ໄດ້_ລາຍງານ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ແລ່ນ()
