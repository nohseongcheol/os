#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. បកប្រែ_ប្រភព 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

បញ្ចាំង_ឬស = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.ផ្លូវ_បញ្ជី = [ទិន្នន័យ.ផ្លូវ for ទិន្នន័យ in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def បង្កើត(자신, ការបញ្ចូល_ចំនុច, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ការវាស់វែង_ផ្លូវ = Path(작업)/'generated.c'
            ពាក្យ_បញ្ជា = ['sh', str(បញ្ចាំង_ឬស/'미리번역.sh'), '--entry', ការបញ្ចូល_ចំនុច,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(ការវាស់វែង_ផ្លូវ)]
            if 범용문자표기: ពាក្យ_បញ្ជា.append('--ucn')
            for កំណត់_តំលៃ in 내보내기목록: ពាក្យ_បញ្ជា.extend(['--export', កំណត់_តំលៃ])
            ពាក្យ_បញ្ជា.extend(str(ផ្លូវ) for ផ្លូវ in 자신.ផ្លូវ_បញ្ជី)
            ការវាស់វែង = subprocess.run(ពាក្យ_បញ្ជា, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ការវាស់វែង.returncode: raise 컴파일오류(ការវាស់វែង.stderr.decode('utf-8', 'replace'))
            return ការវាស់វែង_ផ្លូវ.read_text()

def រត់():
    raise SystemExit(subprocess.call(['sh', str(បញ្ចាំង_ឬស/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': រត់()
