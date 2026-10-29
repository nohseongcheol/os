#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Ittraduċi_sors 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

pprojetta_għerq = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.mogħdija_Lista = [data.mogħdija for data in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def iġġenera(자신, entrata_punt, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            miżura_mogħdija = Path(작업)/'generated.c'
            kmand = ['sh', str(pprojetta_għerq/'미리번역.sh'), '--entry', entrata_punt,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(miżura_mogħdija)]
            if 범용문자표기: kmand.append('--ucn')
            for assenja_VALUE in 내보내기목록: kmand.extend(['--export', assenja_VALUE])
            kmand.extend(str(mogħdija) for mogħdija in 자신.mogħdija_Lista)
            miżura = subprocess.run(kmand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if miżura.returncode: raise 컴파일오류(miżura.stderr.decode('utf-8', 'replace'))
            return miżura_mogħdija.read_text()

def serje():
    raise SystemExit(subprocess.call(['sh', str(pprojetta_għerq/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': serje()
