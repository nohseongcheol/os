#!/usr/bin/env python3
"""OpenJDK와 بومی ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from اجرا_فرمان import نمایش_دادن_جذر


def اجرا_2():
    출력결과 = نمایش_دادن_جذر / 'build/verification/jvm'
    کلاس_مسیر = 출력결과 / 'classes'; کلاس_مسیر.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = نمایش_دادن_جذر / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((نمایش_دادن_جذر / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(کلاس_مسیر)] + [str(رشته_داده_ها) for رشته_داده_ها in 원문목록])
    시험목록 = [('객체시험', ['زمینه_مقدار_0764f371', 'شعبه_مقدار', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['شمارنده_مقدار', 'کار_عمل', 'رشته_مقدار']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ارزیابی_کردن.꾸러미시험', []), ('진입호환시험', [])]
    اعتبارسنجی_گزارش = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for نام, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(کلاس_مسیر) + ':' + str(자바꾸러미), نام], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(نمایش_دادن_جذر / 'ابزارها/اجرا_فایل.py'), str(کلاس_مسیر / (نام.replace('.', '/') + '.class'))]
            if '.' in نام: 명령인수 += ['--class-name', نام]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(کلاس_مسیر / (포함항목 + '.class'))]
            if نام == '한글소스': 명령인수[2] = str(نمایش_دادن_جذر / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            واقعی_سنجش = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (نام + '.log')).write_text(واقعی_سنجش, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", واقعی_سنجش, re.S)
            assert 완료량.returncode == 0 and 일치, (نام, واقعی_سنجش)
            سنجش = next(رشته_داده_ها for رشته_داده_ها in 일치.groups() if رشته_داده_ها is not None) + '\n'
            assert سنجش == 예상결과, (نام, 예상결과, سنجش)
            اعتبارسنجی_گزارش['tests'].append({'name': نام, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', نام, flush=True)
        # بومی JVM에 직접 연결한 فارسی رشته_مقدار/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(نمایش_دادن_جذر/'ابزارها/اجرا_فایل.py'), str(کلاس_مسیر/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        سنجش = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(سنجش)
        assert 완료량.returncode == 0 and 'فارسی 직접 رشته_مقدار هدایت_مقدار\n' in سنجش and '\nexit 0\n' in سنجش, سنجش
        اعتبارسنجی_گزارش['direct_korean_thread_and_entry'] = True
        print('PASS: فارسی 직접 رشته_مقدار·اجرا·اجرا_2 ورودی_نقطه', flush=True)
        유효함 = (کلاس_مسیر / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        اعتبارسنجی_گزارش['rejection_tests'] = []
        for نام, داده_های_ضروری_داده_ها, 알림문 in 시험사례:
            시험자료 = 출력결과 / (نام + '.class'); 시험자료.write_bytes(داده_های_ضروری_داده_ها)
            완료량 = subprocess.run(['python3', str(نمایش_دادن_جذر / 'ابزارها/اجرا_فایل.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            متن = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (نام + '.log')).write_text(متن, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in متن and 'exit 1\n' in متن, (نام, متن)
            اعتبارسنجی_گزارش['rejection_tests'].append({'name': نام, 'passed': True})
            print('PASS (rejected):', نام, flush=True)
        اعتبارسنجی_گزارش['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(اعتبارسنجی_گزارش, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    اجرا_2()
