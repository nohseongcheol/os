#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRANSLATE_kjelde 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

spegle_rot = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.bane_Liste = [data.STIGE for data in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def generere(자신, oppføring_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            forretningsmål_bane = Path(작업)/'generated.c'
            Kommando = ['sh', str(spegle_rot/'미리번역.sh'), '--entry', oppføring_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(forretningsmål_bane)]
            if 범용문자표기: Kommando.append('--ucn')
            for Tilordne_VALUE in 내보내기목록: Kommando.extend(['--export', Tilordne_VALUE])
            Kommando.extend(str(STIGE) for STIGE in 자신.bane_Liste)
            forretningsmål = subprocess.run(Kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if forretningsmål.returncode: raise 컴파일오류(forretningsmål.stderr.decode('utf-8', 'replace'))
            return forretningsmål_bane.read_text()

def Køyr_2():
    raise SystemExit(subprocess.call(['sh', str(spegle_rot/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Køyr_2()
