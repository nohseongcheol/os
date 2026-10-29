#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Þýða_uppruni 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

verk_rót = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.slóð_Listi = [gögn.SLÓÐ for gögn in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def skapa(자신, færsla_P, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            mæld_stærð_slóð = Path(작업)/'generated.c'
            Skipun = ['sh', str(verk_rót/'미리번역.sh'), '--entry', færsla_P,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(mæld_stærð_slóð)]
            if 범용문자표기: Skipun.append('--ucn')
            for úthluta_VALUE in 내보내기목록: Skipun.extend(['--export', úthluta_VALUE])
            Skipun.extend(str(SLÓÐ) for SLÓÐ in 자신.slóð_Listi)
            NIÐURSTAÐA = subprocess.run(Skipun, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if NIÐURSTAÐA.returncode: raise 컴파일오류(NIÐURSTAÐA.stderr.decode('utf-8', 'replace'))
            return mæld_stærð_slóð.read_text()

def Keyra_2():
    raise SystemExit(subprocess.call(['sh', str(verk_rót/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Keyra_2()
