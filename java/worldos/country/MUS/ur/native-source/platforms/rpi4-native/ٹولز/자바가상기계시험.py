#!/usr/bin/env python3
"""OpenJDK와 اپنا ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ


def چلائیں():
    출력결과 = عکس_ڈالنا_روٹ / 'build/verification/jvm'
    صنف_راہ = 출력결과 / 'classes'; صنف_راہ.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = عکس_ڈالنا_روٹ / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((عکس_ڈالنا_روٹ / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(صنف_راہ)] + [str(سلک_کوائف) for سلک_کوائف in 원문목록])
    시험목록 = [('객체시험', ['پس_منظر_قدر', 'برانچ_قدر', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['شمار_کنندہ_قدر', 'ٹاسک_عمل', 'تھریڈ_قدر']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('جواز_دہی_کریں.꾸러미시험', []), ('진입호환시험', [])]
    توثیق_رپورٹ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for نام, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(صنف_راہ) + ':' + str(자바꾸러미), نام], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(عکس_ڈالنا_روٹ / 'ٹولز/نفاذ_کریں_فائل.py'), str(صنف_راہ / (نام.replace('.', '/') + '.class'))]
            if '.' in نام: 명령인수 += ['--class-name', نام]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(صنف_راہ / (포함항목 + '.class'))]
            if نام == '한글소스': 명령인수[2] = str(عکس_ڈالنا_روٹ / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            اصل_پیمائش = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (نام + '.log')).write_text(اصل_پیمائش, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", اصل_پیمائش, re.S)
            assert 완료량.returncode == 0 and 일치, (نام, اصل_پیمائش)
            پیمائش = next(سلک_کوائف for سلک_کوائف in 일치.groups() if سلک_کوائف is not None) + '\n'
            assert پیمائش == 예상결과, (نام, 예상결과, پیمائش)
            توثیق_رپورٹ['tests'].append({'name': نام, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', نام, flush=True)
        # اپنا JVM에 직접 연결한 اردو تھریڈ_قدر/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_فائل.py'), str(صنف_راہ/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        پیمائش = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(پیمائش)
        assert 완료량.returncode == 0 and 'اردو 직접 تھریڈ_قدر ترسیل_کریں_قدر\n' in پیمائش and '\nexit 0\n' in پیمائش, پیمائش
        توثیق_رپورٹ['direct_korean_thread_and_entry'] = True
        print('PASS: اردو 직접 تھریڈ_قدر·اطلاق·چلائیں اندراج_نقطہ', flush=True)
        유효함 = (صنف_راہ / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        توثیق_رپورٹ['rejection_tests'] = []
        for نام, پے_لوڈ_کوائف, 알림문 in 시험사례:
            시험자료 = 출력결과 / (نام + '.class'); 시험자료.write_bytes(پے_لوڈ_کوائف)
            완료량 = subprocess.run(['python3', str(عکس_ڈالنا_روٹ / 'ٹولز/نفاذ_کریں_فائل.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            متن = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (نام + '.log')).write_text(متن, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in متن and 'exit 1\n' in متن, (نام, متن)
            توثیق_رپورٹ['rejection_tests'].append({'name': نام, 'passed': True})
            print('PASS (rejected):', نام, flush=True)
        توثیق_رپورٹ['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(توثیق_رپورٹ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    چلائیں()
