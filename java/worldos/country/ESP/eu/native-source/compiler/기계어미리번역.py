#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. ITZULI_iturburu 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

Project_erro = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.bide_izen_Zerrenda = [datuak.Bide_izena for datuak in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def sortu(자신, sarrera_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            neurria_bide_izen = Path(작업)/'generated.c'
            Komandoa = ['sh', str(Project_erro/'미리번역.sh'), '--entry', sarrera_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(neurria_bide_izen)]
            if 범용문자표기: Komandoa.append('--ucn')
            for Esleitu_balio in 내보내기목록: Komandoa.extend(['--export', Esleitu_balio])
            Komandoa.extend(str(Bide_izena) for Bide_izena in 자신.bide_izen_Zerrenda)
            EMAITZA = subprocess.run(Komandoa, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if EMAITZA.returncode: raise 컴파일오류(EMAITZA.stderr.decode('utf-8', 'replace'))
            return neurria_bide_izen.read_text()

def Exekutatu_2():
    raise SystemExit(subprocess.call(['sh', str(Project_erro/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Exekutatu_2()
