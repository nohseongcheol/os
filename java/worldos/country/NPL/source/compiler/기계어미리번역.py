#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. अनुवाद_स्रोत 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

परियोजना_रूट = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.बाटो_सूची = [लगत.मार्ग for लगत in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def सिर्जना_गर्नुहोस्(자신, प्रविष्टि_अंक, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            मापन_बाटो = Path(작업)/'generated.c'
            आदेश = ['sh', str(परियोजना_रूट/'미리번역.sh'), '--entry', प्रविष्टि_अंक,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(मापन_बाटो)]
            if 범용문자표기: आदेश.append('--ucn')
            for 지정 in 내보내기목록: आदेश.extend(['--export', 지정])
            आदेश.extend(str(मार्ग) for मार्ग in 자신.बाटो_सूची)
            मापन = subprocess.run(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if मापन.returncode: raise 컴파일오류(मापन.stderr.decode('utf-8', 'replace'))
            return मापन_बाटो.read_text()

def चलाउनुहोस्():
    raise SystemExit(subprocess.call(['sh', str(परियोजना_रूट/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': चलाउनुहोस्()
