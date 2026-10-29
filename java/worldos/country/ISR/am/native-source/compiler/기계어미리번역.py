#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. ተርጉም_ምንጭ 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

አሳይ_ስር = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.ዱካ_ዝርዝር = [ውሂብ.መተላለፊያ for ውሂብ in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def አዘጋጅ(자신, ምዝግብ_ቦታ, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ልኬት_ዱካ = Path(작업)/'generated.c'
            ትእዛዝ = ['sh', str(አሳይ_ስር/'미리번역.sh'), '--entry', ምዝግብ_ቦታ,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(ልኬት_ዱካ)]
            if 범용문자표기: ትእዛዝ.append('--ucn')
            for 지정 in 내보내기목록: ትእዛዝ.extend(['--export', 지정])
            ትእዛዝ.extend(str(መተላለፊያ) for መተላለፊያ in 자신.ዱካ_ዝርዝር)
            ልኬት = subprocess.run(ትእዛዝ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ልኬት.returncode: raise 컴파일오류(ልኬት.stderr.decode('utf-8', 'replace'))
            return ልኬት_ዱካ.read_text()

def ማስኬጃ():
    raise SystemExit(subprocess.call(['sh', str(አሳይ_ስር/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': ማስኬጃ()
