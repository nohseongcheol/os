#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. ಅನುವಾದಿಸು_ಮೂಲ 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.ಹಾದಿ_ಪಟ್ಟಿ = [ಡೇಟಾ.ಮಾರ್ಗ for ಡೇಟಾ in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def ರಚಿಸಿ(자신, ನಮೂದು_ಬಿಂದು, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ಮಾಪನ_ಹಾದಿ = Path(작업)/'generated.c'
            ಆಜ್ಞೆ = ['sh', str(ಬಿಂಬಿಸು_ಮೂಲ/'미리번역.sh'), '--entry', ನಮೂದು_ಬಿಂದು,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(ಮಾಪನ_ಹಾದಿ)]
            if 범용문자표기: ಆಜ್ಞೆ.append('--ucn')
            for ನಿಯೋಜಿಸು_ಮೌಲ್ಯ in 내보내기목록: ಆಜ್ಞೆ.extend(['--export', ನಿಯೋಜಿಸು_ಮೌಲ್ಯ])
            ಆಜ್ಞೆ.extend(str(ಮಾರ್ಗ) for ಮಾರ್ಗ in 자신.ಹಾದಿ_ಪಟ್ಟಿ)
            ಮಾಪನ = subprocess.run(ಆಜ್ಞೆ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ಮಾಪನ.returncode: raise 컴파일오류(ಮಾಪನ.stderr.decode('utf-8', 'replace'))
            return ಮಾಪನ_ಹಾದಿ.read_text()

def ಚಲಾಯಿಸು_2():
    raise SystemExit(subprocess.call(['sh', str(ಬಿಂಬಿಸು_ಮೂಲ/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': ಚಲಾಯಿಸು_2()
