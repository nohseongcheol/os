#!/usr/bin/env python3
"""OpenJDK와 eget ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Utfør_kommando import speile_rot


def Kjør_2():
    produksjon = speile_rot / 'build/verification/jvm'
    time_bane = produksjon / 'classes'; time_bane.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = speile_rot / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((speile_rot / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(time_bane)] + [str(streng_data) for streng_data in 원문목록])
    test_Liste = [('객체시험', ['bakgrunn_VERDI', 'gren_VERDI', '계산가능']), ('예외시험', []), ('Samling_test', []),
             ('가닥시험', ['teller_VERDI', 'oppgave_Gjøremål', 'tråd_VERDI']), ('한글시험', []), ('test_Nettverk', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('bekrefte_5fb2b747.test_bunt', []), ('oppføring_kompatibilitet_test', [])]
    validering_rapport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((speile_rot / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Navn, 포함인수 in test_Liste:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(time_bane) + ':' + str(자바꾸러미), Navn], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(speile_rot / 'Verktøy/Utfør_Fil.py'), str(time_bane / (Navn.replace('.', '/') + '.class'))]
            if '.' in Navn: 명령인수 += ['--class-name', Navn]
            for inkludere in 포함인수: 명령인수 += ['--include', str(time_bane / (inkludere + '.class'))]
            if Navn == '한글소스': 명령인수[2] = str(speile_rot / '시험/자바/한글소스.java')
            Fullført_beløp = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            faktisk_KR = Fullført_beløp.stdout.decode('utf-8').replace('\r\n', '\n')
            (produksjon / (Navn + '.log')).write_text(faktisk_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", faktisk_KR, re.S)
            assert Fullført_beløp.returncode == 0 and 일치, (Navn, faktisk_KR)
            KR = next(streng_data for streng_data in 일치.groups() if streng_data is not None) + '\n'
            assert KR == 예상결과, (Navn, 예상결과, KR)
            validering_rapport['tests'].append({'name': Navn, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Navn, flush=True)
        # eget JVM에 직접 연결한 norsk tråd_VERDI/진입점은 OpenJDK용 래퍼가 아니다.
        Fullført_beløp = subprocess.run(['python3', str(speile_rot/'Verktøy/Utfør_Fil.py'), str(time_bane/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        KR = Fullført_beløp.stdout.decode('utf-8').replace('\r\n', '\n')
        (produksjon/'한국어가닥시험.log').write_text(KR)
        assert Fullført_beløp.returncode == 0 and 'norsk 직접 tråd_VERDI sende_VERDI\n' in KR and '\nexit 0\n' in KR, KR
        validering_rapport['direct_korean_thread_and_entry'] = True
        print('PASS: norsk 직접 tråd_VERDI·Kjør·Kjør_2 inngangspunkt', flush=True)
        gyldig = (time_bane / '객체시험.class').read_bytes()
        test_sak = [('판거부', gyldig[:6] + b'\x00\x35' + gyldig[8:], 'supported class versions'),
                 ('잘린클래스', gyldig[:24], 'truncated class file')]
        validering_rapport['rejection_tests'] = []
        for Navn, nyttelast_data, notice_SMS in test_sak:
            test_data = produksjon / (Navn + '.class'); test_data.write_bytes(nyttelast_data)
            Fullført_beløp = subprocess.run(['python3', str(speile_rot / 'Verktøy/Utfør_Fil.py'), str(test_data)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Tekst = Fullført_beløp.stdout.decode('utf-8').replace('\r\n', '\n')
            (produksjon / (Navn + '.log')).write_text(Tekst, encoding='utf-8')
            assert Fullført_beløp.returncode == 1 and notice_SMS in Tekst and 'exit 1\n' in Tekst, (Navn, Tekst)
            validering_rapport['rejection_tests'].append({'name': Navn, 'passed': True})
            print('PASS (rejected):', Navn, flush=True)
        validering_rapport['passed'] = True
    finally:
        (produksjon / 'report.json').write_text(json.dumps(validering_rapport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Kjør_2()
