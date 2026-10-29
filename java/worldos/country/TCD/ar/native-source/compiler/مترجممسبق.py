#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. تحويل_مصدر 구현은 أدواتجافا/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from محول_برمجي import 컴파일오류

يعرض_جذر = Path(__file__).resolve().parent

class جهاز_رمز_محول_برمجي:
    def __init__(자신, 입력클래스들, 실행대상='kernel', كومة_ذاكرة_مؤقتة_عدد_الكلمات=262144):
        자신.مسار_قائمة = [بيانات.مسار for بيانات in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.كومة_ذاكرة_مؤقتة_عدد_الكلمات = كومة_ذاكرة_مؤقتة_عدد_الكلمات

    def إنشاء(자신, نقطة_الإدخال, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            مقياس_مسار = Path(작업)/'generated.c'
            أمر = ['sh', str(يعرض_جذر/'미리번역.sh'), '--entry', نقطة_الإدخال,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.كومة_ذاكرة_مؤقتة_عدد_الكلمات), '-o', str(مقياس_مسار)]
            if 범용문자표기: أمر.append('--ucn')
            for تعيين_قيمة in 내보내기목록: أمر.extend(['--export', تعيين_قيمة])
            أمر.extend(str(مسار) for مسار in 자신.مسار_قائمة)
            نتيجة = subprocess.run(أمر, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if نتيجة.returncode: raise 컴파일오류(نتيجة.stderr.decode('utf-8', 'replace'))
            return مقياس_مسار.read_text()

def تشغيل():
    raise SystemExit(subprocess.call(['sh', str(يعرض_جذر/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': تشغيل()
