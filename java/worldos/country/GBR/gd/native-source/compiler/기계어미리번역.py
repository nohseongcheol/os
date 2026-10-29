#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. TRANSLATE_tùs 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

tilg_freumh = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.slighe_Liosta = [dàta.Slighe for dàta in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def gin(자신, cur_a_steach_puing, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            tomhas_slighe = Path(작업)/'generated.c'
            àithne = ['sh', str(tilg_freumh/'미리번역.sh'), '--entry', cur_a_steach_puing,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(tomhas_slighe)]
            if 범용문자표기: àithne.append('--ucn')
            for 지정 in 내보내기목록: àithne.extend(['--export', 지정])
            àithne.extend(str(Slighe) for Slighe in 자신.slighe_Liosta)
            tomhas = subprocess.run(àithne, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if tomhas.returncode: raise 컴파일오류(tomhas.stderr.decode('utf-8', 'replace'))
            return tomhas_slighe.read_text()

def ruith():
    raise SystemExit(subprocess.call(['sh', str(tilg_freumh/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': ruith()
