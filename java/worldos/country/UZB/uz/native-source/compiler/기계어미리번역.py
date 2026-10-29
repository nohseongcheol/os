#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Tarjima_manba 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

Project_ildiz = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.yo_l_Ro_yxat = [ma_lumotlar.yo_l for ma_lumotlar in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def generatsiiyalash(자신, kiritish_nuqta, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            o_lchov_yo_l = Path(작업)/'generated.c'
            Buyruq = ['sh', str(Project_ildiz/'미리번역.sh'), '--entry', kiritish_nuqta,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(o_lchov_yo_l)]
            if 범용문자표기: Buyruq.append('--ucn')
            for tayinlash_VALUE in 내보내기목록: Buyruq.extend(['--export', tayinlash_VALUE])
            Buyruq.extend(str(yo_l) for yo_l in 자신.yo_l_Ro_yxat)
            o_lchov = subprocess.run(Buyruq, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if o_lchov.returncode: raise 컴파일오류(o_lchov.stderr.decode('utf-8', 'replace'))
            return o_lchov_yo_l.read_text()

def Bajarish():
    raise SystemExit(subprocess.call(['sh', str(Project_ildiz/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Bajarish()
