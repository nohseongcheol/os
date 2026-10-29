#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Пераклад_крыніца 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

기준 = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.шлях_Спіс = [дадзеныя.ШЛЯХ for дадзеныя in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def 생성(자신, увядзенне_бал, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            결과경로 = Path(작업)/'generated.c'
            Загад = ['sh', str(기준/'미리번역.sh'), '--entry', увядзенне_бал,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(결과경로)]
            if 범용문자표기: Загад.append('--ucn')
            for прызначыць_значэнне in 내보내기목록: Загад.extend(['--export', прызначыць_значэнне])
            Загад.extend(str(ШЛЯХ) for ШЛЯХ in 자신.шлях_Спіс)
            결과 = subprocess.run(Загад, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if 결과.returncode: raise 컴파일오류(결과.stderr.decode('utf-8', 'replace'))
            return 결과경로.read_text()

def Выканаць():
    raise SystemExit(subprocess.call(['sh', str(기준/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Выканаць()
