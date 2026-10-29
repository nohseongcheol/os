#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. ترجمہ_ماخذ 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

عکس_ڈالنا_روٹ = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.راہ_فہرست = [کوائف.راستہ_2 for کوائف in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def تخلیق_کرنا(자신, اندراج_نقطہ, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            پیمائش_راہ = Path(작업)/'generated.c'
            حکم = ['sh', str(عکس_ڈالنا_روٹ/'미리번역.sh'), '--entry', اندراج_نقطہ,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(پیمائش_راہ)]
            if 범용문자표기: حکم.append('--ucn')
            for تفویض_کریں_قدر in 내보내기목록: حکم.extend(['--export', تفویض_کریں_قدر])
            حکم.extend(str(راستہ_2) for راستہ_2 in 자신.راہ_فہرست)
            پیمائش = subprocess.run(حکم, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if پیمائش.returncode: raise 컴파일오류(پیمائش.stderr.decode('utf-8', 'replace'))
            return پیمائش_راہ.read_text()

def چلائیں():
    raise SystemExit(subprocess.call(['sh', str(عکس_ڈالنا_روٹ/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': چلائیں()
