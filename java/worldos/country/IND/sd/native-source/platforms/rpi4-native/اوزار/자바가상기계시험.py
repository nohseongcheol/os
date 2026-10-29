#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from تعميل_ڪرڻ_حڪم import 기준


def هلائڻ():
    출력결과 = 기준 / 'build/verification/jvm'
    درجو_راههه = 출력결과 / 'classes'; درجو_راههه.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(درجو_راههه)] + [str(اسٽرنگ_ڪوائف) for اسٽرنگ_ڪوائف in 원문목록])
    시험목록 = [('객체시험', ['پس_منظر_قدر', 'شاخ_قدر', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['ڳڻندڙ_قدر', 'ٽاسڪ_عمل', 'لڙي_قدر']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ڪارگر_ڪريو.꾸러미시험', []), ('진입호환시험', [])]
    ڪارگر_رپورٽ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for نالو, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(درجو_راههه) + ':' + str(자바꾸러미), نالو], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / 'اوزار/تعميل_ڪرڻ_فائل.py'), str(درجو_راههه / (نالو.replace('.', '/') + '.class'))]
            if '.' in نالو: 명령인수 += ['--class-name', نالو]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(درجو_راههه / (포함항목 + '.class'))]
            if نالو == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (نالو + '.log')).write_text(실제결과, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and 일치, (نالو, 실제결과)
            결과 = next(اسٽرنگ_ڪوائف for اسٽرنگ_ڪوائف in 일치.groups() if اسٽرنگ_ڪوائف is not None) + '\n'
            assert 결과 == 예상결과, (نالو, 예상결과, 결과)
            ڪارگر_رپورٽ['tests'].append({'name': نالو, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', نالو, flush=True)
        # 자체 JVM에 직접 연결한 한국어 لڙي_قدر/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'اوزار/تعميل_ڪرڻ_فائل.py'), str(درجو_راههه/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(결과)
        assert 완료량.returncode == 0 and '한국어 직접 لڙي_قدر 통과\n' in 결과 and '\nexit 0\n' in 결과, 결과
        ڪارگر_رپورٽ['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 لڙي_قدر·تعميل_ڪرڻ_ٽاسڪ·هلائڻ داخلا_هنڌ', flush=True)
        유효함 = (درجو_راههه / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        ڪارگر_رپورٽ['rejection_tests'] = []
        for نالو, بنيادي_بار_ڪوائف, 알림문 in 시험사례:
            시험자료 = 출력결과 / (نالو + '.class'); 시험자료.write_bytes(بنيادي_بار_ڪوائف)
            완료량 = subprocess.run(['python3', str(기준 / 'اوزار/تعميل_ڪرڻ_فائل.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            متن = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (نالو + '.log')).write_text(متن, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in متن and 'exit 1\n' in متن, (نالو, متن)
            ڪارگر_رپورٽ['rejection_tests'].append({'name': نالو, 'passed': True})
            print('PASS (rejected):', نالو, flush=True)
        ڪارگر_رپورٽ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(ڪارگر_رپورٽ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    هلائڻ()
