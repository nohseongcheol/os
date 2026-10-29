#!/usr/bin/env python3
"""OpenJDK와 ذاتي ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ينفذ_أمر import يعرض_جذر


def تشغيل():
    الناتج = يعرض_جذر / 'build/verification/jvm'
    فئة_مسار = الناتج / 'classes'; فئة_مسار.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = يعرض_جذر / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((يعرض_جذر / 'اختبارات/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(فئة_مسار)] + [str(سلسلة_بيانات) for سلسلة_بيانات in 원문목록])
    قائمة_الاخبارات = [('객체시험', ['خلفية_قيمة', 'فرع_قيمة', '계산가능']), ('예외시험', []), ('مجموعة_يختبر', []),
             ('가닥시험', ['عدّاد_قيمة', 'مهمة_إجراء', 'محادثة_قيمة']), ('한글시험', []), ('يختبر_شبكات', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('التحقق_من_صحة.يختبر_يُجمع', []), ('إدخال_توافق_يختبر', [])]
    التحقق_من_صحة_إبلاغ = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((يعرض_جذر / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for اسم, 포함인수 in قائمة_الاخبارات:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(فئة_مسار) + ':' + str(자바꾸러미), اسم], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(يعرض_جذر / 'أدوات/ينفذ_ملف.py'), str(فئة_مسار / (اسم.replace('.', '/') + '.class'))]
            if '.' in اسم: 명령인수 += ['--class-name', اسم]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(فئة_مسار / (포함항목 + '.class'))]
            if اسم == '한글소스': 명령인수[2] = str(يعرض_جذر / 'اختبارات/자바/한글소스.java')
            مكتمل_مبلغ = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            الفعلي_مقياس = مكتمل_مبلغ.stdout.decode('utf-8').replace('\r\n', '\n')
            (الناتج / (اسم + '.log')).write_text(الفعلي_مقياس, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", الفعلي_مقياس, re.S)
            assert مكتمل_مبلغ.returncode == 0 and 일치, (اسم, الفعلي_مقياس)
            نتيجة = next(سلسلة_بيانات for سلسلة_بيانات in 일치.groups() if سلسلة_بيانات is not None) + '\n'
            assert نتيجة == 예상결과, (اسم, 예상결과, نتيجة)
            التحقق_من_صحة_إبلاغ['tests'].append({'name': اسم, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', اسم, flush=True)
        # ذاتي JVM에 직접 연결한 العربية محادثة_قيمة/진입점은 OpenJDK용 래퍼가 아니다.
        مكتمل_مبلغ = subprocess.run(['python3', str(يعرض_جذر/'أدوات/ينفذ_ملف.py'), str(فئة_مسار/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        نتيجة = مكتمل_مبلغ.stdout.decode('utf-8').replace('\r\n', '\n')
        (الناتج/'한국어가닥시험.log').write_text(نتيجة)
        assert مكتمل_مبلغ.returncode == 0 and 'العربية 직접 محادثة_قيمة يمرر_قيمة\n' in نتيجة and '\nexit 0\n' in نتيجة, نتيجة
        التحقق_من_صحة_إبلاغ['direct_korean_thread_and_entry'] = True
        print('PASS: العربية 직접 محادثة_قيمة·تنفيذ·تشغيل نقطة_الإدخال', flush=True)
        유효함 = (فئة_مسار / '객체시험.class').read_bytes()
        حالة_اختبار = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        التحقق_من_صحة_إبلاغ['rejection_tests'] = []
        for اسم, حمولة_بيانات, إشعار_نص in حالة_اختبار:
            يختبر_بيانات = الناتج / (اسم + '.class'); يختبر_بيانات.write_bytes(حمولة_بيانات)
            مكتمل_مبلغ = subprocess.run(['python3', str(يعرض_جذر / 'أدوات/ينفذ_ملف.py'), str(يختبر_بيانات)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            نص = مكتمل_مبلغ.stdout.decode('utf-8').replace('\r\n', '\n')
            (الناتج / (اسم + '.log')).write_text(نص, encoding='utf-8')
            assert مكتمل_مبلغ.returncode == 1 and إشعار_نص in نص and 'exit 1\n' in نص, (اسم, نص)
            التحقق_من_صحة_إبلاغ['rejection_tests'].append({'name': اسم, 'passed': True})
            print('PASS (rejected):', اسم, flush=True)
        التحقق_من_صحة_إبلاغ['passed'] = True
    finally:
        (الناتج / 'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    تشغيل()
