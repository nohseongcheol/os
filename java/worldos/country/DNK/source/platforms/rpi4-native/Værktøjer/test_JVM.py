#!/usr/bin/env python3
"""OpenJDK와 eget ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Udfør_kommando import To_do_rod


def Kør_2():
    produktoutput = To_do_rod / 'build/verification/jvm'
    Hold_sti = produktoutput / 'classes'; Hold_sti.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = To_do_rod / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((To_do_rod / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Hold_sti)] + [str(streng_data) for streng_data in 원문목록])
    test_Liste = [('객체시험', ['Baggrund_VÆRDI', 'gren_VÆRDI', '계산가능']), ('예외시험', []), ('Samling_test', []),
             ('가닥시험', ['tæller_VÆRDI', 'job_To_do', 'tråd_VÆRDI']), ('한글시험', []), ('test_Netværk', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('bekræfte_5fb2b747.test_bundt', []), ('post_kompatibilitet_test', [])]
    validering_rapport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((To_do_rod / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Navn, 포함인수 in test_Liste:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Hold_sti) + ':' + str(자바꾸러미), Navn], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(To_do_rod / 'Værktøjer/Udfør_fil.py'), str(Hold_sti / (Navn.replace('.', '/') + '.class'))]
            if '.' in Navn: 명령인수 += ['--class-name', Navn]
            for inkludere in 포함인수: 명령인수 += ['--include', str(Hold_sti / (inkludere + '.class'))]
            if Navn == '한글소스': 명령인수[2] = str(To_do_rod / '시험/자바/한글소스.java')
            fuldført_sum = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            faktisk_KR = fuldført_sum.stdout.decode('utf-8').replace('\r\n', '\n')
            (produktoutput / (Navn + '.log')).write_text(faktisk_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", faktisk_KR, re.S)
            assert fuldført_sum.returncode == 0 and 일치, (Navn, faktisk_KR)
            KR = next(streng_data for streng_data in 일치.groups() if streng_data is not None) + '\n'
            assert KR == 예상결과, (Navn, 예상결과, KR)
            validering_rapport['tests'].append({'name': Navn, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Navn, flush=True)
        # eget JVM에 직접 연결한 Dansk tråd_VÆRDI/진입점은 OpenJDK용 래퍼가 아니다.
        fuldført_sum = subprocess.run(['python3', str(To_do_rod/'Værktøjer/Udfør_fil.py'), str(Hold_sti/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        KR = fuldført_sum.stdout.decode('utf-8').replace('\r\n', '\n')
        (produktoutput/'한국어가닥시험.log').write_text(KR)
        assert fuldført_sum.returncode == 0 and 'Dansk 직접 tråd_VÆRDI videregive_VÆRDI\n' in KR and '\nexit 0\n' in KR, KR
        validering_rapport['direct_korean_thread_and_entry'] = True
        print('PASS: Dansk 직접 tråd_VÆRDI·Kør·Kør_2 indgangspunkt', flush=True)
        gyldig = (Hold_sti / '객체시험.class').read_bytes()
        test_job = [('판거부', gyldig[:6] + b'\x00\x35' + gyldig[8:], 'supported class versions'),
                 ('잘린클래스', gyldig[:24], 'truncated class file')]
        validering_rapport['rejection_tests'] = []
        for Navn, nyttedata_data, 알림문 in test_job:
            test_data = produktoutput / (Navn + '.class'); test_data.write_bytes(nyttedata_data)
            fuldført_sum = subprocess.run(['python3', str(To_do_rod / 'Værktøjer/Udfør_fil.py'), str(test_data)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Tekst = fuldført_sum.stdout.decode('utf-8').replace('\r\n', '\n')
            (produktoutput / (Navn + '.log')).write_text(Tekst, encoding='utf-8')
            assert fuldført_sum.returncode == 1 and 알림문 in Tekst and 'exit 1\n' in Tekst, (Navn, Tekst)
            validering_rapport['rejection_tests'].append({'name': Navn, 'passed': True})
            print('PASS (rejected):', Navn, flush=True)
        validering_rapport['passed'] = True
    finally:
        (produktoutput / 'report.json').write_text(json.dumps(validering_rapport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Kør_2()
