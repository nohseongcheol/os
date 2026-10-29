#!/usr/bin/env python3
"""OpenJDK와 eget ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from köra_kommando import åtgärd_rot


def Kör():
    utleverans = åtgärd_rot / 'build/verification/jvm'
    Kurs_väg = utleverans / 'classes'; Kurs_väg.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = åtgärd_rot / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((åtgärd_rot / 'tester/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Kurs_väg)] + [str(sträng_data) for sträng_data in 원문목록])
    test_ange = [('객체시험', ['Bakgrund_värde', 'gren_värde', '계산가능']), ('예외시험', []), ('mängd_test', []),
             ('가닥시험', ['räknare_värde', 'uppgift_Action', 'tråd_värde']), ('한글시험', []), ('test_Nätverk', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('validera.test_bunt', []), ('post_kompatibilitet_test', [])]
    validering_Rapport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((åtgärd_rot / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Namn, 포함인수 in test_ange:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Kurs_väg) + ':' + str(자바꾸러미), Namn], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(åtgärd_rot / 'verktyg/köra_fil.py'), str(Kurs_väg / (Namn.replace('.', '/') + '.class'))]
            if '.' in Namn: 명령인수 += ['--class-name', Namn]
            for ta_med in 포함인수: 명령인수 += ['--include', str(Kurs_väg / (ta_med + '.class'))]
            if Namn == '한글소스': 명령인수[2] = str(åtgärd_rot / 'tester/자바/한글소스.java')
            Slutfört_belopp = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            verklig_KR = Slutfört_belopp.stdout.decode('utf-8').replace('\r\n', '\n')
            (utleverans / (Namn + '.log')).write_text(verklig_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", verklig_KR, re.S)
            assert Slutfört_belopp.returncode == 0 and 일치, (Namn, verklig_KR)
            RESULTAT = next(sträng_data for sträng_data in 일치.groups() if sträng_data is not None) + '\n'
            assert RESULTAT == 예상결과, (Namn, 예상결과, RESULTAT)
            validering_Rapport['tests'].append({'name': Namn, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Namn, flush=True)
        # eget JVM에 직접 연결한 Svenska tråd_värde/진입점은 OpenJDK용 래퍼가 아니다.
        Slutfört_belopp = subprocess.run(['python3', str(åtgärd_rot/'verktyg/köra_fil.py'), str(Kurs_väg/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        RESULTAT = Slutfört_belopp.stdout.decode('utf-8').replace('\r\n', '\n')
        (utleverans/'한국어가닥시험.log').write_text(RESULTAT)
        assert Slutfört_belopp.returncode == 0 and 'Svenska 직접 tråd_värde skicka_värde\n' in RESULTAT and '\nexit 0\n' in RESULTAT, RESULTAT
        validering_Rapport['direct_korean_thread_and_entry'] = True
        print('PASS: Svenska 직접 tråd_värde·Starta·Kör startpunkt', flush=True)
        giltig = (Kurs_väg / '객체시험.class').read_bytes()
        test_akt = [('판거부', giltig[:6] + b'\x00\x35' + giltig[8:], 'supported class versions'),
                 ('잘린클래스', giltig[:24], 'truncated class file')]
        validering_Rapport['rejection_tests'] = []
        for Namn, nyttolast_data, 알림문 in test_akt:
            test_data = utleverans / (Namn + '.class'); test_data.write_bytes(nyttolast_data)
            Slutfört_belopp = subprocess.run(['python3', str(åtgärd_rot / 'verktyg/köra_fil.py'), str(test_data)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            text = Slutfört_belopp.stdout.decode('utf-8').replace('\r\n', '\n')
            (utleverans / (Namn + '.log')).write_text(text, encoding='utf-8')
            assert Slutfört_belopp.returncode == 1 and 알림문 in text and 'exit 1\n' in text, (Namn, text)
            validering_Rapport['rejection_tests'].append({'name': Namn, 'passed': True})
            print('PASS (rejected):', Namn, flush=True)
        validering_Rapport['passed'] = True
    finally:
        (utleverans / 'report.json').write_text(json.dumps(validering_Rapport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Kör()
