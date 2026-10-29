#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. अनुवाद_स्रोत 구현은 जावासाधन/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from कंपाइलर import संकलन_त्रुटि

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parent

class यंत्र_कोड_कंपाइलर:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.पथ_सूची = [आँकड़े.पथ for आँकड़े in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def जनरेट_करें(자신, प्रवेश_बिदुं, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            परिणाम_पथ = Path(작업)/'generated.c'
            आदेश = ['sh', str(प्रोजेक्ट_करें_मूल/'미리번역.sh'), '--entry', प्रवेश_बिदुं,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(परिणाम_पथ)]
            if 범용문자표기: आदेश.append('--ucn')
            for असाइन_करें_मान in 내보내기목록: आदेश.extend(['--export', असाइन_करें_मान])
            आदेश.extend(str(पथ) for पथ in 자신.पथ_सूची)
            परिणाम = subprocess.run(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if परिणाम.returncode: raise संकलन_त्रुटि(परिणाम.stderr.decode('utf-8', 'replace'))
            return परिणाम_पथ.read_text()

def चलाएँ():
    raise SystemExit(subprocess.call(['sh', str(प्रोजेक्ट_करें_मूल/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': चलाएँ()
