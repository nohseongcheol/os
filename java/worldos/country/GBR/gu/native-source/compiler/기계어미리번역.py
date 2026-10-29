#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. અનુવાદ_કરો_સ્રોત 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.પાથ_સૂચી = [ડેટા.પથ for ડેટા in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def જનરેટ_કરો(자신, પ્રવેશ_બિંદુ, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            પરિમાણ_પાથ = Path(작업)/'generated.c'
            આદેશ = ['sh', str(પ્રોજેક્ટ_રૂટ/'미리번역.sh'), '--entry', પ્રવેશ_બિંદુ,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(પરિમાણ_પાથ)]
            if 범용문자표기: આદેશ.append('--ucn')
            for 지정 in 내보내기목록: આદેશ.extend(['--export', 지정])
            આદેશ.extend(str(પથ) for પથ in 자신.પાથ_સૂચી)
            પરિમાણ = subprocess.run(આદેશ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if પરિમાણ.returncode: raise 컴파일오류(પરિમાણ.stderr.decode('utf-8', 'replace'))
            return પરિમાણ_પાથ.read_text()

def ચલાવો_2():
    raise SystemExit(subprocess.call(['sh', str(પ્રોજેક્ટ_રૂટ/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': ચલાવો_2()
