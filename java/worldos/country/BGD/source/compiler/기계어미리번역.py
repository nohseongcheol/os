#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. অনুবাদ_করুন_উত্স 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

প্রকল্প_মূল = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.পথ_তালিকা = [ডাটা.পথ_2 for ডাটা in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def সৃষ্টি_করুন(자신, ভুক্তি_বিন্দু, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            পরিমাপ_পথ = Path(작업)/'generated.c'
            আদেশ = ['sh', str(প্রকল্প_মূল/'미리번역.sh'), '--entry', ভুক্তি_বিন্দু,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(পরিমাপ_পথ)]
            if 범용문자표기: আদেশ.append('--ucn')
            for নিয়োগ_করুন_মান in 내보내기목록: আদেশ.extend(['--export', নিয়োগ_করুন_মান])
            আদেশ.extend(str(পথ_2) for পথ_2 in 자신.পথ_তালিকা)
            পরিমাপ = subprocess.run(আদেশ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if পরিমাপ.returncode: raise 컴파일오류(পরিমাপ.stderr.decode('utf-8', 'replace'))
            return পরিমাপ_পথ.read_text()

def চালনা():
    raise SystemExit(subprocess.call(['sh', str(প্রকল্প_মূল/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': চালনা()
