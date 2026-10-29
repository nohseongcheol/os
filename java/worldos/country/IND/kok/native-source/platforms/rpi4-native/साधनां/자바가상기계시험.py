#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट


def चलोवप():
    출력결과 = प्रॉजॅक्ट_रूट / 'build/verification/jvm'
    वर्ग_पाथ = 출력결과 / 'classes'; वर्ग_पाथ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = प्रॉजॅक्ट_रूट / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((प्रॉजॅक्ट_रूट / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(वर्ग_पाथ)] + [str(स्ट्रिंग_डेटा) for स्ट्रिंग_डेटा in 원문목록])
    시험목록 = [('객체시험', ['फाटभूंय_मोल', 'शाखा_मोल', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['काउंटर_मोल', 'कार्य_कृती', 'थ्रॅड_मोल']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('पुनर्तपासणी_करची_5fb2b747.꾸러미시험', []), ('진입호환시험', [])]
    वैधताय_अहवाल = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for नांव, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(वर्ग_पाथ) + ':' + str(자바꾸러미), नांव], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(प्रॉजॅक्ट_रूट / 'साधनां/पाळो_दिवचो_फायल.py'), str(वर्ग_पाथ / (नांव.replace('.', '/') + '.class'))]
            if '.' in नांव: 명령인수 += ['--class-name', नांव]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(वर्ग_पाथ / (포함항목 + '.class'))]
            if नांव == '한글소스': 명령인수[2] = str(प्रॉजॅक्ट_रूट / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            प्रत्यक्ष_मेजप = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (नांव + '.log')).write_text(प्रत्यक्ष_मेजप, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", प्रत्यक्ष_मेजप, re.S)
            assert 완료량.returncode == 0 and 일치, (नांव, प्रत्यक्ष_मेजप)
            मेजप = next(स्ट्रिंग_डेटा for स्ट्रिंग_डेटा in 일치.groups() if स्ट्रिंग_डेटा is not None) + '\n'
            assert मेजप == 예상결과, (नांव, 예상결과, मेजप)
            वैधताय_अहवाल['tests'].append({'name': नांव, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', नांव, flush=True)
        # 자체 JVM에 직접 연결한 한국어 थ्रॅड_मोल/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_फायल.py'), str(वर्ग_पाथ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        मेजप = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(मेजप)
        assert 완료량.returncode == 0 and '한국어 직접 थ्रॅड_मोल पास_मोल\n' in मेजप and '\nexit 0\n' in मेजप, मेजप
        वैधताय_अहवाल['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 थ्रॅड_मोल·पाळो_दिवचो_कार्य·चलोवप प्रवेश_पॉयंट', flush=True)
        유효함 = (वर्ग_पाथ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        वैधताय_अहवाल['rejection_tests'] = []
        for नांव, पेलोड_डेटा, 알림문 in 시험사례:
            시험자료 = 출력결과 / (नांव + '.class'); 시험자료.write_bytes(पेलोड_डेटा)
            완료량 = subprocess.run(['python3', str(प्रॉजॅक्ट_रूट / 'साधनां/पाळो_दिवचो_फायल.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (नांव + '.log')).write_text(SMS, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in SMS and 'exit 1\n' in SMS, (नांव, SMS)
            वैधताय_अहवाल['rejection_tests'].append({'name': नांव, 'passed': True})
            print('PASS (rejected):', नांव, flush=True)
        वैधताय_अहवाल['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(वैधताय_अहवाल, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    चलोवप()
