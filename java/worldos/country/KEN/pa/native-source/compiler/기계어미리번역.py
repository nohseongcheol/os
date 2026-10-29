#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. ਅਨੁਵਾਦ_ਸਰੋਤ 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.ਰਸਤਾ_ਸੂਚੀ = [ਸਮੱਗਰੀ.ਮਾਰਗ for ਸਮੱਗਰੀ in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def ਜਨਰੇਟ_ਕਰੋ(자신, ਦਾਖਲਾ_ਪੌਇੰਟ, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ਮਾਪ_ਰਸਤਾ = Path(작업)/'generated.c'
            ਕਮਾਂਡ = ['sh', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'미리번역.sh'), '--entry', ਦਾਖਲਾ_ਪੌਇੰਟ,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(ਮਾਪ_ਰਸਤਾ)]
            if 범용문자표기: ਕਮਾਂਡ.append('--ucn')
            for ਅਸਾਈਨ_ਕਰੋ_ਕੀਮਤ in 내보내기목록: ਕਮਾਂਡ.extend(['--export', ਅਸਾਈਨ_ਕਰੋ_ਕੀਮਤ])
            ਕਮਾਂਡ.extend(str(ਮਾਰਗ) for ਮਾਰਗ in 자신.ਰਸਤਾ_ਸੂਚੀ)
            ਮਾਪ = subprocess.run(ਕਮਾਂਡ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ਮਾਪ.returncode: raise 컴파일오류(ਮਾਪ.stderr.decode('utf-8', 'replace'))
            return ਮਾਪ_ਰਸਤਾ.read_text()

def ਚਲਾਓ_2():
    raise SystemExit(subprocess.call(['sh', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': ਚਲਾਓ_2()
