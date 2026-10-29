#!/usr/bin/env python3
"""OpenJDK와 ίδιο ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from εκτελώ_εντολή import έργο_ρίζα


def Εκτέλεση_2():
    출력결과 = έργο_ρίζα / 'build/verification/jvm'
    Τάξη_διαδρομή = 출력결과 / 'classes'; Τάξη_διαδρομή.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = έργο_ρίζα / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((έργο_ρίζα / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Τάξη_διαδρομή)] + [str(συμβολοσειρά_δεδομένα) for συμβολοσειρά_δεδομένα in 원문목록])
    λίστα_δοκιμών = [('객체시험', ['φόντο_τιμή', 'κλάδος_τιμή', '계산가능']), ('예외시험', []), ('πλήθος_δοκιμή', []),
             ('가닥시험', ['μετρητής_τιμή', 'εργασία_έργο', 'νήμα_τιμή']), ('한글시험', []), ('δοκιμή_Δικτύωση', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('επικυρώνω.δοκιμή_πακέτο', []), ('καταχώρηση_συμβατότητα_δοκιμή', [])]
    επικύρωση_έκθεση = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((έργο_ρίζα / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Όνομα, 포함인수 in λίστα_δοκιμών:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Τάξη_διαδρομή) + ':' + str(자바꾸러미), Όνομα], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(έργο_ρίζα / 'Εργαλεία/εκτελώ_Αρχείο.py'), str(Τάξη_διαδρομή / (Όνομα.replace('.', '/') + '.class'))]
            if '.' in Όνομα: 명령인수 += ['--class-name', Όνομα]
            for περιλαμβάνω in 포함인수: 명령인수 += ['--include', str(Τάξη_διαδρομή / (περιλαμβάνω + '.class'))]
            if Όνομα == '한글소스': 명령인수[2] = str(έργο_ρίζα / '시험/자바/한글소스.java')
            Ολοκληρωμένες_ποσό = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            πραγματικός_μέτρηση = Ολοκληρωμένες_ποσό.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Όνομα + '.log')).write_text(πραγματικός_μέτρηση, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", πραγματικός_μέτρηση, re.S)
            assert Ολοκληρωμένες_ποσό.returncode == 0 and 일치, (Όνομα, πραγματικός_μέτρηση)
            μέτρηση = next(συμβολοσειρά_δεδομένα for συμβολοσειρά_δεδομένα in 일치.groups() if συμβολοσειρά_δεδομένα is not None) + '\n'
            assert μέτρηση == 예상결과, (Όνομα, 예상결과, μέτρηση)
            επικύρωση_έκθεση['tests'].append({'name': Όνομα, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Όνομα, flush=True)
        # ίδιο JVM에 직접 연결한 ελληνικά νήμα_τιμή/진입점은 OpenJDK용 래퍼가 아니다.
        Ολοκληρωμένες_ποσό = subprocess.run(['python3', str(έργο_ρίζα/'Εργαλεία/εκτελώ_Αρχείο.py'), str(Τάξη_διαδρομή/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        μέτρηση = Ολοκληρωμένες_ποσό.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(μέτρηση)
        assert Ολοκληρωμένες_ποσό.returncode == 0 and 'ελληνικά 직접 νήμα_τιμή διαβιβάζω_τιμή\n' in μέτρηση and '\nexit 0\n' in μέτρηση, μέτρηση
        επικύρωση_έκθεση['direct_korean_thread_and_entry'] = True
        print('PASS: ελληνικά 직접 νήμα_τιμή·Εκτέλεση·Εκτέλεση_2 σημείο_εισόδου', flush=True)
        έγγυρος = (Τάξη_διαδρομή / '객체시험.class').read_bytes()
        υπόθεση_δοκιμής = [('판거부', έγγυρος[:6] + b'\x00\x35' + έγγυρος[8:], 'supported class versions'),
                 ('잘린클래스', έγγυρος[:24], 'truncated class file')]
        επικύρωση_έκθεση['rejection_tests'] = []
        for Όνομα, ωφέλιμο_φορτίο_δεδομένα, γνωστοποίηση_μήνυμα in υπόθεση_δοκιμής:
            δοκιμή_δεδομένα = 출력결과 / (Όνομα + '.class'); δοκιμή_δεδομένα.write_bytes(ωφέλιμο_φορτίο_δεδομένα)
            Ολοκληρωμένες_ποσό = subprocess.run(['python3', str(έργο_ρίζα / 'Εργαλεία/εκτελώ_Αρχείο.py'), str(δοκιμή_δεδομένα)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Κείμενο = Ολοκληρωμένες_ποσό.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Όνομα + '.log')).write_text(Κείμενο, encoding='utf-8')
            assert Ολοκληρωμένες_ποσό.returncode == 1 and γνωστοποίηση_μήνυμα in Κείμενο and 'exit 1\n' in Κείμενο, (Όνομα, Κείμενο)
            επικύρωση_έκθεση['rejection_tests'].append({'name': Όνομα, 'passed': True})
            print('PASS (rejected):', Όνομα, flush=True)
        επικύρωση_έκθεση['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(επικύρωση_έκθεση, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Εκτέλεση_2()
