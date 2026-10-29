#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. अणकारप_स्त्रोत 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.पाथ_सुची = [डेटा.पाथ for डेटा in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def तयार_करचें(자신, प्रवेश_पॉयंट, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            मेजप_पाथ = Path(작업)/'generated.c'
            आदेश = ['sh', str(प्रॉजॅक्ट_रूट/'미리번역.sh'), '--entry', प्रवेश_पॉयंट,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(मेजप_पाथ)]
            if 범용문자표기: आदेश.append('--ucn')
            for 지정 in 내보내기목록: आदेश.extend(['--export', 지정])
            आदेश.extend(str(पाथ) for पाथ in 자신.पाथ_सुची)
            मेजप = subprocess.run(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if मेजप.returncode: raise 컴파일오류(मेजप.stderr.decode('utf-8', 'replace'))
            return मेजप_पाथ.read_text()

def चलोवप():
    raise SystemExit(subprocess.call(['sh', str(प्रॉजॅक्ट_रूट/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': चलोवप()
