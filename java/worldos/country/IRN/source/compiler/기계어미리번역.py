#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. تبدیل_منبع 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

نمایش_دادن_جذر = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.مسیر_لیست = [داده_ها.مسیر for داده_ها in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def ایجاد(자신, ورودی_نقطه, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            سنجش_مسیر = Path(작업)/'generated.c'
            فرمان = ['sh', str(نمایش_دادن_جذر/'미리번역.sh'), '--entry', ورودی_نقطه,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(سنجش_مسیر)]
            if 범용문자표기: فرمان.append('--ucn')
            for اختصاص_مقدار in 내보내기목록: فرمان.extend(['--export', اختصاص_مقدار])
            فرمان.extend(str(مسیر) for مسیر in 자신.مسیر_لیست)
            سنجش = subprocess.run(فرمان, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if سنجش.returncode: raise 컴파일오류(سنجش.stderr.decode('utf-8', 'replace'))
            return سنجش_مسیر.read_text()

def اجرا_2():
    raise SystemExit(subprocess.call(['sh', str(نمایش_دادن_جذر/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': اجرا_2()
