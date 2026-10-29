#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRADUEIX_font 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

Project_rel = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.camí_Llista = [dades.Camí for dades in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def generar(자신, introducció_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            mesura_camí = Path(작업)/'generated.c'
            Ordre = ['sh', str(Project_rel/'미리번역.sh'), '--entry', introducció_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(mesura_camí)]
            if 범용문자표기: Ordre.append('--ucn')
            for cedir_VALOR in 내보내기목록: Ordre.extend(['--export', cedir_VALOR])
            Ordre.extend(str(Camí) for Camí in 자신.camí_Llista)
            RESULTAT = subprocess.run(Ordre, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if RESULTAT.returncode: raise 컴파일오류(RESULTAT.stderr.decode('utf-8', 'replace'))
            return mesura_camí.read_text()

def Executa_2():
    raise SystemExit(subprocess.call(['sh', str(Project_rel/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Executa_2()
