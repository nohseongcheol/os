#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Превод_източник 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from компилатор import грешка_при_компилиране

проект_корен = Path(__file__).resolve().parent

class машина_код_компилатор:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.път_Списък = [данни.ПЪТ for данни in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def генерирам(자신, запис_пункт, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            мярка_път = Path(작업)/'generated.c'
            Команда = ['sh', str(проект_корен/'미리번역.sh'), '--entry', запис_пункт,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(мярка_път)]
            if 범용문자표기: Команда.append('--ucn')
            for Възложи_стойност in 내보내기목록: Команда.extend(['--export', Възложи_стойност])
            Команда.extend(str(ПЪТ) for ПЪТ in 자신.път_Списък)
            РЕЗУЛТАТ = subprocess.run(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if РЕЗУЛТАТ.returncode: raise грешка_при_компилиране(РЕЗУЛТАТ.stderr.decode('utf-8', 'replace'))
            return мярка_път.read_text()

def Стартиране():
    raise SystemExit(subprocess.call(['sh', str(проект_корен/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Стартиране()
