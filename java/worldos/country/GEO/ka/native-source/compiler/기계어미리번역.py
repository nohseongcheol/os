#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. თარგმნა_წყარო 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

პროეცირება_ფესვი = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.მდებარეობა_სია = [მონაცემები.გეზი for მონაცემები in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def დაგენერირება(자신, შენატანი_პტ, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            გაზომვა_მდებარეობა = Path(작업)/'generated.c'
            ბრძანება = ['sh', str(პროეცირება_ფესვი/'미리번역.sh'), '--entry', შენატანი_პტ,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(გაზომვა_მდებარეობა)]
            if 범용문자표기: ბრძანება.append('--ucn')
            for 지정 in 내보내기목록: ბრძანება.extend(['--export', 지정])
            ბრძანება.extend(str(გეზი) for გეზი in 자신.მდებარეობა_სია)
            გაზომვა = subprocess.run(ბრძანება, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if გაზომვა.returncode: raise 컴파일오류(გაზომვა.stderr.decode('utf-8', 'replace'))
            return გაზომვა_მდებარეობა.read_text()

def გაშვება():
    raise SystemExit(subprocess.call(['sh', str(პროეცირება_ფესვი/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': გაშვება()
