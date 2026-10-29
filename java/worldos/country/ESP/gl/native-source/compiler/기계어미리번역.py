#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRADUCIR_fonte 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

Project_raíz = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.camiño_Lista = [datos.CAMIÑO for datos in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def xerar(자신, introdución_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            medida_camiño = Path(작업)/'generated.c'
            Orde = ['sh', str(Project_raíz/'미리번역.sh'), '--entry', introdución_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(medida_camiño)]
            if 범용문자표기: Orde.append('--ucn')
            for Asignar_VALOR in 내보내기목록: Orde.extend(['--export', Asignar_VALOR])
            Orde.extend(str(CAMIÑO) for CAMIÑO in 자신.camiño_Lista)
            RESULTANTE = subprocess.run(Orde, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if RESULTANTE.returncode: raise 컴파일오류(RESULTANTE.stderr.decode('utf-8', 'replace'))
            return medida_camiño.read_text()

def Executar_2():
    raise SystemExit(subprocess.call(['sh', str(Project_raíz/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Executar_2()
