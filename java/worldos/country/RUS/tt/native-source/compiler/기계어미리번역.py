#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRANSLATE_чыганак 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

экранга_җибәрү_тамыр = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.юл_Исемлек_4d1a5003 = [мәгълүмат.Yul for мәгълүмат in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def булдыру(자신, кертү_балл, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            үлчәм_юл = Path(작업)/'generated.c'
            команда = ['sh', str(экранга_җибәрү_тамыр/'미리번역.sh'), '--entry', кертү_балл,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(үлчәм_юл)]
            if 범용문자표기: команда.append('--ucn')
            for 지정 in 내보내기목록: команда.extend(['--export', 지정])
            команда.extend(str(Yul) for Yul in 자신.юл_Исемлек_4d1a5003)
            үлчәм = subprocess.run(команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if үлчәм.returncode: raise 컴파일오류(үлчәм.stderr.decode('utf-8', 'replace'))
            return үлчәм_юл.read_text()

def эшләтү():
    raise SystemExit(subprocess.call(['sh', str(экранга_җибәрү_тамыр/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': эшләтү()
