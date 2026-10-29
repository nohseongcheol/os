#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ausféieren_Befeel import projezéieren_Racinn


def Laf():
    출력결과 = projezéieren_Racinn / 'build/verification/jvm'
    Klass_Wee = 출력결과 / 'classes'; Klass_Wee.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = projezéieren_Racinn / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((projezéieren_Racinn / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Klass_Wee)] + [str(Zeechefolleg_Daten) for Zeechefolleg_Daten in 원문목록])
    시험목록 = [('객체시험', ['Hannergrond_VALUE', 'Branche_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['Zieler_VALUE', 'To_do_Aktioun', 'Thread_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('validéieren.꾸러미시험', []), ('진입호환시험', [])]
    Validatioun_mellen = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((projezéieren_Racinn / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Numm, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Klass_Wee) + ':' + str(자바꾸러미), Numm], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(projezéieren_Racinn / 'Tools/ausféieren_Fichier.py'), str(Klass_Wee / (Numm.replace('.', '/') + '.class'))]
            if '.' in Numm: 명령인수 += ['--class-name', Numm]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(Klass_Wee / (포함항목 + '.class'))]
            if Numm == '한글소스': 명령인수[2] = str(projezéieren_Racinn / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            aktuell_Mooss = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Numm + '.log')).write_text(aktuell_Mooss, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", aktuell_Mooss, re.S)
            assert 완료량.returncode == 0 and 일치, (Numm, aktuell_Mooss)
            Mooss = next(Zeechefolleg_Daten for Zeechefolleg_Daten in 일치.groups() if Zeechefolleg_Daten is not None) + '\n'
            assert Mooss == 예상결과, (Numm, 예상결과, Mooss)
            Validatioun_mellen['tests'].append({'name': Numm, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Numm, flush=True)
        # 자체 JVM에 직접 연결한 한국어 Thread_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(projezéieren_Racinn/'Tools/ausféieren_Fichier.py'), str(Klass_Wee/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        Mooss = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(Mooss)
        assert 완료량.returncode == 0 and '한국어 직접 Thread_VALUE iwwermëttelen_VALUE\n' in Mooss and '\nexit 0\n' in Mooss, Mooss
        Validatioun_mellen['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 Thread_VALUE·Ausféieren·Laf Agab_Punkt', flush=True)
        유효함 = (Klass_Wee / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        Validatioun_mellen['rejection_tests'] = []
        for Numm, nëtzlech_Charge_Daten, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Numm + '.class'); 시험자료.write_bytes(nëtzlech_Charge_Daten)
            완료량 = subprocess.run(['python3', str(projezéieren_Racinn / 'Tools/ausféieren_Fichier.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Numm + '.log')).write_text(SMS, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in SMS and 'exit 1\n' in SMS, (Numm, SMS)
            Validatioun_mellen['rejection_tests'].append({'name': Numm, 'passed': True})
            print('PASS (rejected):', Numm, flush=True)
        Validatioun_mellen['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(Validatioun_mellen, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Laf()
