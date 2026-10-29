#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Prevedi_izvor 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

projicirati_koijen = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.put_spisak = [podaci.Putanja for podaci in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def generirati(자신, unos_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            mjera_put = Path(작업)/'generated.c'
            Naredba = ['sh', str(projicirati_koijen/'미리번역.sh'), '--entry', unos_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(mjera_put)]
            if 범용문자표기: Naredba.append('--ucn')
            for dodijeliti_VALUE in 내보내기목록: Naredba.extend(['--export', dodijeliti_VALUE])
            Naredba.extend(str(Putanja) for Putanja in 자신.put_spisak)
            mjera = subprocess.run(Naredba, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if mjera.returncode: raise 컴파일오류(mjera.stderr.decode('utf-8', 'replace'))
            return mjera_put.read_text()

def Pokreni():
    raise SystemExit(subprocess.call(['sh', str(projicirati_koijen/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Pokreni()
