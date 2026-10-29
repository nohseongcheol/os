#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Cyfieithu_ffynhonnell 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

prosiect_gwraidd = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.llwybr_Rhestr = [data.LLWYBR for data in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def cynhyrchu(자신, cofnod_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            mesur_llwybr = Path(작업)/'generated.c'
            Gorchymyn = ['sh', str(prosiect_gwraidd/'미리번역.sh'), '--entry', cofnod_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(mesur_llwybr)]
            if 범용문자표기: Gorchymyn.append('--ucn')
            for 지정 in 내보내기목록: Gorchymyn.extend(['--export', 지정])
            Gorchymyn.extend(str(LLWYBR) for LLWYBR in 자신.llwybr_Rhestr)
            mesur = subprocess.run(Gorchymyn, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if mesur.returncode: raise 컴파일오류(mesur.stderr.decode('utf-8', 'replace'))
            return mesur_llwybr.read_text()

def Gweithredu_2():
    raise SystemExit(subprocess.call(['sh', str(prosiect_gwraidd/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Gweithredu_2()
