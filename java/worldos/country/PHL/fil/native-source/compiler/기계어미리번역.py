#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRANSLATE_pinagmulan 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

Project_root = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.path_list = [data.path for data in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def mag_generate(자신, pagpasok_point, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            sukat_path = Path(작업)/'generated.c'
            utos = ['sh', str(Project_root/'미리번역.sh'), '--entry', pagpasok_point,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(sukat_path)]
            if 범용문자표기: utos.append('--ucn')
            for italaga_VALUE in 내보내기목록: utos.extend(['--export', italaga_VALUE])
            utos.extend(str(path) for path in 자신.path_list)
            sukat = subprocess.run(utos, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if sukat.returncode: raise 컴파일오류(sukat.stderr.decode('utf-8', 'replace'))
            return sukat_path.read_text()

def run():
    raise SystemExit(subprocess.call(['sh', str(Project_root/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': run()
