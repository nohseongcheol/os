#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. ଅନୁବାଦ_ଉତ୍ସ 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.ପଥ_ତାଲିକା = [ଡାଟା.ପଥ for ଡାଟା in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def ସୃଷ୍ଟି_କରିବା(자신, ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ମାପ_ପଥ = Path(작업)/'generated.c'
            ନିର୍ଦ୍ଦେଶ = ['sh', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'미리번역.sh'), '--entry', ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(ମାପ_ପଥ)]
            if 범용문자표기: ନିର୍ଦ୍ଦେଶ.append('--ucn')
            for ନ୍ୟସ୍ତ_କରିବା_ମୂଲ୍ୟ in 내보내기목록: ନିର୍ଦ୍ଦେଶ.extend(['--export', ନ୍ୟସ୍ତ_କରିବା_ମୂଲ୍ୟ])
            ନିର୍ଦ୍ଦେଶ.extend(str(ପଥ) for ପଥ in 자신.ପଥ_ତାଲିକା)
            ମାପ = subprocess.run(ନିର୍ଦ୍ଦେଶ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ମାପ.returncode: raise 컴파일오류(ମାପ.stderr.decode('utf-8', 'replace'))
            return ମାପ_ପଥ.read_text()

def ଚଳାନ୍ତୁ():
    raise SystemExit(subprocess.call(['sh', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': ଚଳାନ୍ତୁ()
