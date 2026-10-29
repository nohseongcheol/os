#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from নিষ্পাদন_আদেশ import 기준


def সঞ্চালন():
    출력결과 = 기준 / 'build/verification/jvm'
    শ্ৰেণী_পথ = 출력결과 / 'classes'; শ্ৰেণী_পথ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(শ্ৰেণী_পথ)] + [str(ষ্ট্ৰিং_ডাটা) for ষ্ট্ৰিং_ডাটা in 원문목록])
    시험목록 = [('객체시험', ['পটভূমি_মান', 'শাখা_মান', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['কাউণ্টাৰ_মান', 'কার্য্য_কাৰ্য', 'আঁহ_মান']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('বৈধকৰণ_কৰক.꾸러미시험', []), ('진입호환시험', [])]
    বৈধতা_ৰিপ_ৰ্ট = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for নাম, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(শ্ৰেণী_পথ) + ':' + str(자바꾸러미), নাম], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / 'সঁজুলিসমূহ/নিষ্পাদন_ফাইল.py'), str(শ্ৰেণী_পথ / (নাম.replace('.', '/') + '.class'))]
            if '.' in নাম: 명령인수 += ['--class-name', নাম]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(শ্ৰেণী_পথ / (포함항목 + '.class'))]
            if নাম == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            প্ৰকৃত_পৰিমাপ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (নাম + '.log')).write_text(প্ৰকৃত_পৰিমাপ, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", প্ৰকৃত_পৰিমাপ, re.S)
            assert 완료량.returncode == 0 and 일치, (নাম, প্ৰকৃত_পৰিমাপ)
            পৰিমাপ = next(ষ্ট্ৰিং_ডাটা for ষ্ট্ৰিং_ডাটা in 일치.groups() if ষ্ট্ৰিং_ডাটা is not None) + '\n'
            assert পৰিমাপ == 예상결과, (নাম, 예상결과, পৰিমাপ)
            বৈধতা_ৰিপ_ৰ্ট['tests'].append({'name': নাম, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', নাম, flush=True)
        # 자체 JVM에 직접 연결한 한국어 আঁহ_মান/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'সঁজুলিসমূহ/নিষ্পাদন_ফাইল.py'), str(শ্ৰেণী_পথ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        পৰিমাপ = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(পৰিমাপ)
        assert 완료량.returncode == 0 and '한국어 직접 আঁহ_মান পাছ_মান\n' in পৰিমাপ and '\nexit 0\n' in পৰিমাপ, পৰিমাপ
        বৈধতা_ৰিপ_ৰ্ট['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 আঁহ_মান·চলাওক·সঞ্চালন প্রবিষ্ট_পইণ্ট', flush=True)
        유효함 = (শ্ৰেণী_পথ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        বৈধতা_ৰিপ_ৰ্ট['rejection_tests'] = []
        for নাম, প্লেল_ড_ডাটা, 알림문 in 시험사례:
            시험자료 = 출력결과 / (নাম + '.class'); 시험자료.write_bytes(প্লেল_ড_ডাটা)
            완료량 = subprocess.run(['python3', str(기준 / 'সঁজুলিসমূহ/নিষ্পাদন_ফাইল.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            টেক্সট = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (নাম + '.log')).write_text(টেক্সট, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in টেক্সট and 'exit 1\n' in টেক্সট, (নাম, টেক্সট)
            বৈধতা_ৰিপ_ৰ্ট['rejection_tests'].append({'name': নাম, 'passed': True})
            print('PASS (rejected):', নাম, flush=True)
        বৈধতা_ৰিপ_ৰ্ট['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    সঞ্চালন()
