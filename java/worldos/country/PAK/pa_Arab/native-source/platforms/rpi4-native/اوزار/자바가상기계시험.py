#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from نفاذ_کرو_حکم import 기준


def چلاؤ():
    출력결과 = 기준 / 'build/verification/jvm'
    درجہ_راہ = 출력결과 / 'classes'; درجہ_راہ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = 기준 / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((기준 / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(درجہ_راہ)] + [str(سٹرنگ_کوائف) for سٹرنگ_کوائف in 원문목록])
    시험목록 = [('객체시험', ['پس_منظر_قدر', 'شاخ_قدر', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['شمار_کرنڑ_آلا_قدر', 'ٹاسک_کم', 'لڑی_قدر']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('تریخ_دے_مطابق_کرو.꾸러미시험', []), ('진입호환시험', [])]
    جواز_دہی_رپورٹ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ناں, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(درجہ_راہ) + ':' + str(자바꾸러미), ناں], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(기준 / 'اوزار/نفاذ_کرو_فائل.py'), str(درجہ_راہ / (ناں.replace('.', '/') + '.class'))]
            if '.' in ناں: 명령인수 += ['--class-name', ناں]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(درجہ_راہ / (포함항목 + '.class'))]
            if ناں == '한글소스': 명령인수[2] = str(기준 / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            실제결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ناں + '.log')).write_text(실제결과, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 실제결과, re.S)
            assert 완료량.returncode == 0 and 일치, (ناں, 실제결과)
            결과 = next(سٹرنگ_کوائف for سٹرنگ_کوائف in 일치.groups() if سٹرنگ_کوائف is not None) + '\n'
            assert 결과 == 예상결과, (ناں, 예상결과, 결과)
            جواز_دہی_رپورٹ['tests'].append({'name': ناں, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ناں, flush=True)
        # 자체 JVM에 직접 연결한 한국어 لڑی_قدر/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(기준/'اوزار/نفاذ_کرو_فائل.py'), str(درجہ_راہ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        결과 = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(결과)
        assert 완료량.returncode == 0 and '한국어 직접 لڑی_قدر پاس_قدر\n' in 결과 and '\nexit 0\n' in 결과, 결과
        جواز_دہی_رپورٹ['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 لڑی_قدر·نفاذ_کرو_ٹاسک·چلاؤ داخلہ_مقام', flush=True)
        유효함 = (درجہ_راہ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        جواز_دہی_رپورٹ['rejection_tests'] = []
        for ناں, پے_لوڈ_کوائف, 알림문 in 시험사례:
            시험자료 = 출력결과 / (ناں + '.class'); 시험자료.write_bytes(پے_لوڈ_کوائف)
            완료량 = subprocess.run(['python3', str(기준 / 'اوزار/نفاذ_کرو_فائل.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            متن = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ناں + '.log')).write_text(متن, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in متن and 'exit 1\n' in متن, (ناں, متن)
            جواز_دہی_رپورٹ['rejection_tests'].append({'name': ناں, 'passed': True})
            print('PASS (rejected):', ناں, flush=True)
        جواز_دہی_رپورٹ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(جواز_دہی_رپورٹ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    چلاؤ()
