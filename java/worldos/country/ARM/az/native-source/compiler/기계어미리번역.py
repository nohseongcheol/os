#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRANSLATE_mənbə 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

Project_kök = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.yol_Siyahı = [verilənlər.Cığır for verilənlər in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def yarat(자신, daxiletmə_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ölçü_yol = Path(작업)/'generated.c'
            Əmr = ['sh', str(Project_kök/'미리번역.sh'), '--entry', daxiletmə_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(ölçü_yol)]
            if 범용문자표기: Əmr.append('--ucn')
            for təyin_et_VALUE in 내보내기목록: Əmr.extend(['--export', təyin_et_VALUE])
            Əmr.extend(str(Cığır) for Cığır in 자신.yol_Siyahı)
            ölçü = subprocess.run(Əmr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ölçü.returncode: raise 컴파일오류(ölçü.stderr.decode('utf-8', 'replace'))
            return ölçü_yol.read_text()

def İcra_Et():
    raise SystemExit(subprocess.call(['sh', str(Project_kök/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': İcra_Et()
