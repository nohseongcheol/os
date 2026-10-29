#!/usr/bin/env python3
"""OpenJDK와 निज ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल


def चलाएँ():
    출력결과 = प्रोजेक्ट_करें_मूल / 'build/verification/jvm'
    कक्षा_पथ = 출력결과 / 'classes'; कक्षा_पथ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = प्रोजेक्ट_करें_मूल / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((प्रोजेक्ट_करें_मूल / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(कक्षा_पथ)] + [str(स्ट्रिंग_डेटा) for स्ट्रिंग_डेटा in 원문목록])
    परिक्षण_सूची = [('객체시험', ['वॉलपेपर_मान', 'शाखा_मान', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['काउंटर_मान', 'कार्य_एक्शन', 'थ्रेड_मान']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('मान्य_करें.꾸러미시험', []), ('진입호환시험', [])]
    प्रमाणीकरण_रिपोर्ट = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((प्रोजेक्ट_करें_मूल / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for नाम, 포함인수 in परिक्षण_सूची:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(कक्षा_पथ) + ':' + str(자바꾸러미), नाम], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(प्रोजेक्ट_करें_मूल / 'उपकरण/निष्पादित_करें_फ़ाइल.py'), str(कक्षा_पथ / (नाम.replace('.', '/') + '.class'))]
            if '.' in नाम: 명령인수 += ['--class-name', नाम]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(कक्षा_पथ / (포함항목 + '.class'))]
            if नाम == '한글소스': 명령인수[2] = str(प्रोजेक्ट_करें_मूल / '시험/자바/한글소스.java')
            पूर्ण_राशि = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            वास्तविक_परिणाम = पूर्ण_राशि.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (नाम + '.log')).write_text(वास्तविक_परिणाम, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", वास्तविक_परिणाम, re.S)
            assert पूर्ण_राशि.returncode == 0 and 일치, (नाम, वास्तविक_परिणाम)
            परिणाम = next(स्ट्रिंग_डेटा for स्ट्रिंग_डेटा in 일치.groups() if स्ट्रिंग_डेटा is not None) + '\n'
            assert परिणाम == 예상결과, (नाम, 예상결과, परिणाम)
            प्रमाणीकरण_रिपोर्ट['tests'].append({'name': नाम, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', नाम, flush=True)
        # निज JVM에 직접 연결한 हिंदी थ्रेड_मान/진입점은 OpenJDK용 래퍼가 아니다.
        पूर्ण_राशि = subprocess.run(['python3', str(प्रोजेक्ट_करें_मूल/'उपकरण/निष्पादित_करें_फ़ाइल.py'), str(कक्षा_पथ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        परिणाम = पूर्ण_राशि.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(परिणाम)
        assert पूर्ण_राशि.returncode == 0 and 'हिंदी 직접 थ्रेड_मान पास_करें_मान\n' in परिणाम and '\nexit 0\n' in परिणाम, परिणाम
        प्रमाणीकरण_रिपोर्ट['direct_korean_thread_and_entry'] = True
        print('PASS: हिंदी 직접 थ्रेड_मान·निष्पादन·चलाएँ प्रवेश_बिदुं', flush=True)
        वैध = (कक्षा_पथ / '객체시험.class').read_bytes()
        परिक्षण_विषय = [('판거부', वैध[:6] + b'\x00\x35' + वैध[8:], 'supported class versions'),
                 ('잘린클래스', वैध[:24], 'truncated class file')]
        प्रमाणीकरण_रिपोर्ट['rejection_tests'] = []
        for नाम, पेलोड_डेटा, सूचना_पाठ in परिक्षण_विषय:
            시험자료 = 출력결과 / (नाम + '.class'); 시험자료.write_bytes(पेलोड_डेटा)
            पूर्ण_राशि = subprocess.run(['python3', str(प्रोजेक्ट_करें_मूल / 'उपकरण/निष्पादित_करें_फ़ाइल.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            पाठ = पूर्ण_राशि.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (नाम + '.log')).write_text(पाठ, encoding='utf-8')
            assert पूर्ण_राशि.returncode == 1 and सूचना_पाठ in पाठ and 'exit 1\n' in पाठ, (नाम, पाठ)
            प्रमाणीकरण_रिपोर्ट['rejection_tests'].append({'name': नाम, 'passed': True})
            print('PASS (rejected):', नाम, flush=True)
        प्रमाणीकरण_रिपोर्ट['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    चलाएँ()
