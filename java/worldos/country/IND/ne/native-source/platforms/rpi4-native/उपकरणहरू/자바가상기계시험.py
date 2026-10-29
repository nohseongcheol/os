#!/usr/bin/env python3
"""OpenJDK와 निज ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट


def चलाउनुहोस्():
    출력결과 = परियोजना_रूट / 'build/verification/jvm'
    वर्ग_बाटो = 출력결과 / 'classes'; वर्ग_बाटो.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = परियोजना_रूट / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((परियोजना_रूट / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(वर्ग_बाटो)] + [str(स्ट्रिङ_लगत) for स्ट्रिङ_लगत in 원문목록])
    시험목록 = [('객체시험', ['वालपेपर_मान', 'शाखा_मान', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['बाह्य_आकृति_मान', 'कार्य_कार्य', 'धागो_मान']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('वैध_गर्नुहोस्.꾸러미시험', []), ('진입호환시험', [])]
    वैधानिकता_रिपोर्ट = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((परियोजना_रूट / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for नाम, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(वर्ग_बाटो) + ':' + str(자바꾸러미), नाम], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(परियोजना_रूट / 'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_फाइल.py'), str(वर्ग_बाटो / (नाम.replace('.', '/') + '.class'))]
            if '.' in नाम: 명령인수 += ['--class-name', नाम]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(वर्ग_बाटो / (포함항목 + '.class'))]
            if नाम == '한글소스': 명령인수[2] = str(परियोजना_रूट / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            वास्तविक_मापन = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (नाम + '.log')).write_text(वास्तविक_मापन, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", वास्तविक_मापन, re.S)
            assert 완료량.returncode == 0 and 일치, (नाम, वास्तविक_मापन)
            मापन = next(स्ट्रिङ_लगत for स्ट्रिङ_लगत in 일치.groups() if स्ट्रिङ_लगत is not None) + '\n'
            assert मापन == 예상결과, (नाम, 예상결과, मापन)
            वैधानिकता_रिपोर्ट['tests'].append({'name': नाम, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', नाम, flush=True)
        # निज JVM에 직접 연결한 नेपाली धागो_मान/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_फाइल.py'), str(वर्ग_बाटो/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        मापन = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(मापन)
        assert 완료량.returncode == 0 and 'नेपाली 직접 धागो_मान पास_मान\n' in मापन and '\nexit 0\n' in मापन, मापन
        वैधानिकता_रिपोर्ट['direct_korean_thread_and_entry'] = True
        print('PASS: नेपाली 직접 धागो_मान·कार्यान्वयन_गर्नुहोस्·चलाउनुहोस् प्रविष्टि_अंक', flush=True)
        유효함 = (वर्ग_बाटो / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        वैधानिकता_रिपोर्ट['rejection_tests'] = []
        for नाम, पेलोड_लगत, 알림문 in 시험사례:
            시험자료 = 출력결과 / (नाम + '.class'); 시험자료.write_bytes(पेलोड_लगत)
            완료량 = subprocess.run(['python3', str(परियोजना_रूट / 'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_फाइल.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            पाठ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (नाम + '.log')).write_text(पाठ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in पाठ and 'exit 1\n' in पाठ, (नाम, पाठ)
            वैधानिकता_रिपोर्ट['rejection_tests'].append({'name': नाम, 'passed': True})
            print('PASS (rejected):', नाम, flush=True)
        वैधानिकता_रिपोर्ट['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    चलाउनुहोस्()
