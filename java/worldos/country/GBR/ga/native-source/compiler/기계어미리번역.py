#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Aistrigh_foinse 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

teilgean_fréamh = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.cosán_Liosta = [sonraí.CONAIR for sonraí in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def giniúint(자신, iontráil_pointe, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            tomhas_cosán = Path(작업)/'generated.c'
            Ordú = ['sh', str(teilgean_fréamh/'미리번역.sh'), '--entry', iontráil_pointe,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(tomhas_cosán)]
            if 범용문자표기: Ordú.append('--ucn')
            for 지정 in 내보내기목록: Ordú.extend(['--export', 지정])
            Ordú.extend(str(CONAIR) for CONAIR in 자신.cosán_Liosta)
            tomhas = subprocess.run(Ordú, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if tomhas.returncode: raise 컴파일오류(tomhas.stderr.decode('utf-8', 'replace'))
            return tomhas_cosán.read_text()

def Rith_2():
    raise SystemExit(subprocess.call(['sh', str(teilgean_fréamh/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Rith_2()
