#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Vertaal_bron 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

Project_wortel = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.pad_Lys = [data.Pad for data in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def genereer(자신, inskrywing_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            maatreël_pad = Path(작업)/'generated.c'
            Opdrag = ['sh', str(Project_wortel/'미리번역.sh'), '--entry', inskrywing_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(maatreël_pad)]
            if 범용문자표기: Opdrag.append('--ucn')
            for toeken_VALUE in 내보내기목록: Opdrag.extend(['--export', toeken_VALUE])
            Opdrag.extend(str(Pad) for Pad in 자신.pad_Lys)
            maatreël = subprocess.run(Opdrag, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if maatreël.returncode: raise 컴파일오류(maatreël.stderr.decode('utf-8', 'replace'))
            return maatreël_pad.read_text()

def Loop():
    raise SystemExit(subprocess.call(['sh', str(Project_wortel/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Loop()
