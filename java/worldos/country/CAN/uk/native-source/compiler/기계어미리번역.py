#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Перекласти_джерело 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from компілятор import помилка_компіляції

Дії_корінь = Path(__file__).resolve().parent

class комп_ютер_код_компілятор:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.шлях_список = [дані.шлях for дані in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def генерувати(자신, запис_бал, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            КР_шлях = Path(작업)/'generated.c'
            команда = ['sh', str(Дії_корінь/'미리번역.sh'), '--entry', запис_бал,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(КР_шлях)]
            if 범용문자표기: команда.append('--ucn')
            for Призначити_значення in 내보내기목록: команда.extend(['--export', Призначити_значення])
            команда.extend(str(шлях) for шлях in 자신.шлях_список)
            результат = subprocess.run(команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if результат.returncode: raise помилка_компіляції(результат.stderr.decode('utf-8', 'replace'))
            return КР_шлях.read_text()

def запустити():
    raise SystemExit(subprocess.call(['sh', str(Дії_корінь/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': запустити()
