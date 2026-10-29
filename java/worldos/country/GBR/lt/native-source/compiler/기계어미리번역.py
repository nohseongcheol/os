#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Versti_šaltinis 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kompiliatorius import kompiliavimo_klaida

Project_šaknis = Path(__file__).resolve().parent

class mašina_CODE_kompiliatorius:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.kelias_Sąrašas = [duomenys.KELIAS for duomenys in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def generuoti(자신, įrašas_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_kelias = Path(작업)/'generated.c'
            Komanda = ['sh', str(Project_šaknis/'미리번역.sh'), '--entry', įrašas_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(KR_kelias)]
            if 범용문자표기: Komanda.append('--ucn')
            for Priskirti_VALUE in 내보내기목록: Komanda.extend(['--export', Priskirti_VALUE])
            Komanda.extend(str(KELIAS) for KELIAS in 자신.kelias_Sąrašas)
            REZULTATAS = subprocess.run(Komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if REZULTATAS.returncode: raise kompiliavimo_klaida(REZULTATAS.stderr.decode('utf-8', 'replace'))
            return KR_kelias.read_text()

def Paleisti():
    raise SystemExit(subprocess.call(['sh', str(Project_šaknis/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Paleisti()
