#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRANSLATE_pūtake 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

whakaatu_pūtake = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.ara_Rārangi = [raraunga.ara for raraunga in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def waihanga(자신, tāurunga_ira, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            mēhua_ara = Path(작업)/'generated.c'
            tono = ['sh', str(whakaatu_pūtake/'미리번역.sh'), '--entry', tāurunga_ira,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(mēhua_ara)]
            if 범용문자표기: tono.append('--ucn')
            for tautapa_uara in 내보내기목록: tono.extend(['--export', tautapa_uara])
            tono.extend(str(ara) for ara in 자신.ara_Rārangi)
            mēhua = subprocess.run(tono, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if mēhua.returncode: raise 컴파일오류(mēhua.stderr.decode('utf-8', 'replace'))
            return mēhua_ara.read_text()

def whakahaere():
    raise SystemExit(subprocess.call(['sh', str(whakaatu_pūtake/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': whakahaere()
