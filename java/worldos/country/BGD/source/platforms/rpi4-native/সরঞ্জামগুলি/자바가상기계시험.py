#!/usr/bin/env python3
"""OpenJDK와 নিজ ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল


def চালনা():
    출력결과 = প্রকল্প_মূল / 'build/verification/jvm'
    শ্রেণী_পথ = 출력결과 / 'classes'; শ্রেণী_পথ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = প্রকল্প_মূল / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((প্রকল্প_মূল / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(শ্রেণী_পথ)] + [str(স্ট্রিং_ডাটা) for স্ট্রিং_ডাটা in 원문목록])
    시험목록 = [('객체시험', ['পটভূমি_মান', 'শাখা_মান', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['গণক_মান', 'কার্য_কর্ম', 'থ্রেড_মান']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('বৈধ_করুন.꾸러미시험', []), ('진입호환시험', [])]
    বৈধকরণ_রিপোর্ট = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((প্রকল্প_মূল / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for নাম, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(শ্রেণী_পথ) + ':' + str(자바꾸러미), নাম], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(প্রকল্প_মূল / 'সরঞ্জামগুলি/কার্যকর_করুন_ফাইল.py'), str(শ্রেণী_পথ / (নাম.replace('.', '/') + '.class'))]
            if '.' in নাম: 명령인수 += ['--class-name', নাম]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(শ্রেণী_পথ / (포함항목 + '.class'))]
            if নাম == '한글소스': 명령인수[2] = str(প্রকল্প_মূল / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            প্রকৃত_পরিমাপ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (নাম + '.log')).write_text(প্রকৃত_পরিমাপ, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", প্রকৃত_পরিমাপ, re.S)
            assert 완료량.returncode == 0 and 일치, (নাম, প্রকৃত_পরিমাপ)
            পরিমাপ = next(স্ট্রিং_ডাটা for স্ট্রিং_ডাটা in 일치.groups() if স্ট্রিং_ডাটা is not None) + '\n'
            assert পরিমাপ == 예상결과, (নাম, 예상결과, পরিমাপ)
            বৈধকরণ_রিপোর্ট['tests'].append({'name': নাম, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', নাম, flush=True)
        # নিজ JVM에 직접 연결한 বাংলা থ্রেড_মান/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(প্রকল্প_মূল/'সরঞ্জামগুলি/কার্যকর_করুন_ফাইল.py'), str(শ্রেণী_পথ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        পরিমাপ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(পরিমাপ)
        assert 완료량.returncode == 0 and 'বাংলা 직접 থ্রেড_মান পাস_মান\n' in পরিমাপ and '\nexit 0\n' in পরিমাপ, পরিমাপ
        বৈধকরণ_রিপোর্ট['direct_korean_thread_and_entry'] = True
        print('PASS: বাংলা 직접 থ্রেড_মান·চালানো·চালনা ভুক্তি_বিন্দু', flush=True)
        유효함 = (শ্রেণী_পথ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        বৈধকরণ_রিপোর্ট['rejection_tests'] = []
        for নাম, পেলোড_ডাটা, 알림문 in 시험사례:
            시험자료 = 출력결과 / (নাম + '.class'); 시험자료.write_bytes(পেলোড_ডাটা)
            완료량 = subprocess.run(['python3', str(প্রকল্প_মূল / 'সরঞ্জামগুলি/কার্যকর_করুন_ফাইল.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            পাঠ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (নাম + '.log')).write_text(পাঠ, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in পাঠ and 'exit 1\n' in পাঠ, (নাম, পাঠ)
            বৈধকরণ_রিপোর্ট['rejection_tests'].append({'name': নাম, 'passed': True})
            print('PASS (rejected):', নাম, flush=True)
        বৈধকরণ_রিপোর্ট['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    চালনা()
