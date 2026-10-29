#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Превод_извор 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

Project_корен = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.патека_Список = [податоци.ПАТЕКА for податоци in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def генерира(자신, внес_поен, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            мерка_патека = Path(작업)/'generated.c'
            Команда = ['sh', str(Project_корен/'미리번역.sh'), '--entry', внес_поен,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(мерка_патека)]
            if 범용문자표기: Команда.append('--ucn')
            for доделува_VALUE in 내보내기목록: Команда.extend(['--export', доделува_VALUE])
            Команда.extend(str(ПАТЕКА) for ПАТЕКА in 자신.патека_Список)
            мерка = subprocess.run(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if мерка.returncode: raise 컴파일오류(мерка.stderr.decode('utf-8', 'replace'))
            return мерка_патека.read_text()

def Изврши_2():
    raise SystemExit(subprocess.call(['sh', str(Project_корен/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Изврши_2()
