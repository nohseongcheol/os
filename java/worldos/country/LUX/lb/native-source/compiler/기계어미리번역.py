#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRANSLATE_Quell 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

projezéieren_Racinn = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.Wee_Lëscht = [Daten.Wee for Daten in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def generéieren(자신, Agab_Punkt, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            Mooss_Wee = Path(작업)/'generated.c'
            Befeel = ['sh', str(projezéieren_Racinn/'미리번역.sh'), '--entry', Agab_Punkt,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(Mooss_Wee)]
            if 범용문자표기: Befeel.append('--ucn')
            for 지정 in 내보내기목록: Befeel.extend(['--export', 지정])
            Befeel.extend(str(Wee) for Wee in 자신.Wee_Lëscht)
            Mooss = subprocess.run(Befeel, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if Mooss.returncode: raise 컴파일오류(Mooss.stderr.decode('utf-8', 'replace'))
            return Mooss_Wee.read_text()

def Laf():
    raise SystemExit(subprocess.call(['sh', str(projezéieren_Racinn/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Laf()
