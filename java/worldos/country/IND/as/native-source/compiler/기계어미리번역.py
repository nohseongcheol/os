#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. অনুবাদ_উৎস 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

기준 = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.পথ_সূচী = [ডাটা.পথ for ডাটা in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def সৃষ্টি_কৰক(자신, প্রবিষ্ট_পইণ্ট, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            পৰিমাপ_পথ = Path(작업)/'generated.c'
            কমান্ড = ['sh', str(기준/'미리번역.sh'), '--entry', প্রবিষ্ট_পইণ্ট,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(পৰিমাপ_পথ)]
            if 범용문자표기: কমান্ড.append('--ucn')
            for 지정 in 내보내기목록: কমান্ড.extend(['--export', 지정])
            কমান্ড.extend(str(পথ) for পথ in 자신.পথ_সূচী)
            পৰিমাপ = subprocess.run(কমান্ড, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if পৰিমাপ.returncode: raise 컴파일오류(পৰিমাপ.stderr.decode('utf-8', 'replace'))
            return পৰিমাপ_পথ.read_text()

def সঞ্চালন():
    raise SystemExit(subprocess.call(['sh', str(기준/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': সঞ্চালন()
