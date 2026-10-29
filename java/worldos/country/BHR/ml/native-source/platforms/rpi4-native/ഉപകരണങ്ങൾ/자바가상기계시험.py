#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം


def നടപ്പിലാക്കുക():
    출력결과 = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/verification/jvm'
    ക്ലാസ്_പാത = 출력결과 / 'classes'; ക്ലാസ്_പാത.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(ക്ലാസ്_പാത)] + [str(സ്ട്രിംഗ്_ഡാറ്റാ) for സ്ട്രിംഗ്_ഡാറ്റാ in 원문목록])
    പരിശോധന_ലിസ്റ്റ് = [('객체시험', ['నేపథ్యం_മൂല്യം', 'ശാഖ_മൂല്യം', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['కౌంటర్_മൂല്യം', 'ചുമതല_ക്രിയ', 'ത്രെഡ്_മൂല്യം']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('സാധൂകരിക്കുക.꾸러미시험', []), ('진입호환시험', [])]
    నిర్ధారణ_నివేదిక = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for പേരു്, 포함인수 in പരിശോധന_ലിസ്റ്റ്:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ക്ലാസ്_പാത) + ':' + str(자바꾸러미), പേരു്], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_ഫയല്.py'), str(ക്ലാസ്_പാത / (പേരു്.replace('.', '/') + '.class'))]
            if '.' in പേരു്: 명령인수 += ['--class-name', പേരു്]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(ക്ലാസ്_പാത / (포함항목 + '.class'))]
            if പേരു് == '한글소스': 명령인수[2] = str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            വാസ്തവമായ_അളവ് = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (പേരു് + '.log')).write_text(വാസ്തവമായ_അളവ്, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", വാസ്തവമായ_അളവ്, re.S)
            assert 완료량.returncode == 0 and 일치, (പേരു്, വാസ്തവമായ_അളവ്)
            അളവ് = next(സ്ട്രിംഗ്_ഡാറ്റാ for സ്ട്രിംഗ്_ഡാറ്റാ in 일치.groups() if സ്ട്രിംഗ്_ഡാറ്റാ is not None) + '\n'
            assert അളവ് == 예상결과, (പേരു്, 예상결과, അളവ്)
            నిర్ధారణ_నివేదిక['tests'].append({'name': പേരു്, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', പേരു്, flush=True)
        # 자체 JVM에 직접 연결한 한국어 ത്രെഡ്_മൂല്യം/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_ഫയല്.py'), str(ക്ലാസ്_പാത/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        അളവ് = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(അളവ്)
        assert 완료량.returncode == 0 and '한국어 직접 ത്രെഡ്_മൂല്യം കൈമാറുക_മൂല്യം\n' in അളവ് and '\nexit 0\n' in അളവ്, അളവ്
        నిర్ధారణ_నివేదిక['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 ത്രെഡ്_മൂല്യം·പ്രവര്_ത്തിപ്പിയ്ക്കുക·നടപ്പിലാക്കുക എന്_ട്രി_പോയിന്_റ്', flush=True)
        സാധുതയുളള = (ക്ലാസ്_പാത / '객체시험.class').read_bytes()
        കേസ്_പരിശോധന = [('판거부', സാധുതയുളള[:6] + b'\x00\x35' + സാധുതയുളള[8:], 'supported class versions'),
                 ('잘린클래스', സാധുതയുളള[:24], 'truncated class file')]
        నిర్ధారణ_నివేదిక['rejection_tests'] = []
        for പേരു്, പേലോഡ്_ഡാറ്റാ, 알림문 in കേസ്_പരിശോധന:
            시험자료 = 출력결과 / (പേരു് + '.class'); 시험자료.write_bytes(പേലോഡ്_ഡാറ്റാ)
            완료량 = subprocess.run(['python3', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_ഫയല്.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            പദാവലി = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (പേരു് + '.log')).write_text(പദാവലി, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in പദാവലി and 'exit 1\n' in പദാവലി, (പേരു്, പദാവലി)
            నిర్ధారణ_నివేదిక['rejection_tests'].append({'name': പേരു്, 'passed': True})
            print('PASS (rejected):', പേരു്, flush=True)
        నిర్ధారణ_నివేదిక['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
