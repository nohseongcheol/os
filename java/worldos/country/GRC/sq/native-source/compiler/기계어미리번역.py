#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Përkthe_burim 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

Project_rrënjë = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.shteg_Listë = [të_dhëna.POZICIONI for të_dhëna in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def gjeneroj(자신, futje_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            llogaritje_shteg = Path(작업)/'generated.c'
            Komanda = ['sh', str(Project_rrënjë/'미리번역.sh'), '--entry', futje_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(llogaritje_shteg)]
            if 범용문자표기: Komanda.append('--ucn')
            for cakto_VALUE in 내보내기목록: Komanda.extend(['--export', cakto_VALUE])
            Komanda.extend(str(POZICIONI) for POZICIONI in 자신.shteg_Listë)
            llogaritje = subprocess.run(Komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if llogaritje.returncode: raise 컴파일오류(llogaritje.stderr.decode('utf-8', 'replace'))
            return llogaritje_shteg.read_text()

def Ekzekuto():
    raise SystemExit(subprocess.call(['sh', str(Project_rrënjë/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Ekzekuto()
