#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. превести_извор 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

пројектовати_корен = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.пут_Листа = [подаци.ПУТАЊА for подаци in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def генерисати(자신, унос_поен, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            мера_пут = Path(작업)/'generated.c'
            Наредба = ['sh', str(пројектовати_корен/'미리번역.sh'), '--entry', унос_поен,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(мера_пут)]
            if 범용문자표기: Наредба.append('--ucn')
            for Додели_вриједност in 내보내기목록: Наредба.extend(['--export', Додели_вриједност])
            Наредба.extend(str(ПУТАЊА) for ПУТАЊА in 자신.пут_Листа)
            ИСХОД = subprocess.run(Наредба, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ИСХОД.returncode: raise 컴파일오류(ИСХОД.stderr.decode('utf-8', 'replace'))
            return мера_пут.read_text()

def Покрени():
    raise SystemExit(subprocess.call(['sh', str(пројектовати_корен/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Покрени()
