#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. تەرجىمە_مەنبە 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.يول_تىزىم = [مەلۇمات.يول for مەلۇمات in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def ھاسىل_قىلىش(자신, كىرگۈزۈش_نوقتا, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ئۆلچەم_يول = Path(작업)/'generated.c'
            بۇيرۇق = ['sh', str(كۆرسىتىش_يىلتىز/'미리번역.sh'), '--entry', كىرگۈزۈش_نوقتا,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(ئۆلچەم_يول)]
            if 범용문자표기: بۇيرۇق.append('--ucn')
            for 지정 in 내보내기목록: بۇيرۇق.extend(['--export', 지정])
            بۇيرۇق.extend(str(يول) for يول in 자신.يول_تىزىم)
            ئۆلچەم = subprocess.run(بۇيرۇق, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ئۆلچەم.returncode: raise 컴파일오류(ئۆلچەم.stderr.decode('utf-8', 'replace'))
            return ئۆلچەم_يول.read_text()

def ئىجرا_قىل_2():
    raise SystemExit(subprocess.call(['sh', str(كۆرسىتىش_يىلتىز/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': ئىجرا_قىل_2()
