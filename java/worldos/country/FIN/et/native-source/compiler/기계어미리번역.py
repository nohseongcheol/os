#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Tõlgi_lähe 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kompilaator import kompileerimistõrge

Project_juur = Path(__file__).resolve().parent

class arvuti_CODE_kompilaator:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.tee_Loend = [andmed.RADA for andmed in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def genereerima(자신, kirje_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            näitaja_tee = Path(작업)/'generated.c'
            Käsk = ['sh', str(Project_juur/'미리번역.sh'), '--entry', kirje_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(näitaja_tee)]
            if 범용문자표기: Käsk.append('--ucn')
            for Määra_VALUE in 내보내기목록: Käsk.extend(['--export', Määra_VALUE])
            Käsk.extend(str(RADA) for RADA in 자신.tee_Loend)
            TULEMUS = subprocess.run(Käsk, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if TULEMUS.returncode: raise kompileerimistõrge(TULEMUS.stderr.decode('utf-8', 'replace'))
            return näitaja_tee.read_text()

def Käivita_2():
    raise SystemExit(subprocess.call(['sh', str(Project_juur/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Käivita_2()
