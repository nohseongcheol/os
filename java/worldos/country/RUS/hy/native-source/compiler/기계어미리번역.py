#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Թարգմանել_աղբյուր 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

արձակել_արմատ = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.ուղի_Ցուցակ = [տվյալ.Ճանապարհ for տվյալ in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def արտադրել(자신, մուտքագրում_կետ, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            չափ_ուղի = Path(작업)/'generated.c'
            Հրահանգ = ['sh', str(արձակել_արմատ/'미리번역.sh'), '--entry', մուտքագրում_կետ,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(չափ_ուղի)]
            if 범용문자표기: Հրահանգ.append('--ucn')
            for 지정 in 내보내기목록: Հրահանգ.extend(['--export', 지정])
            Հրահանգ.extend(str(Ճանապարհ) for Ճանապարհ in 자신.ուղի_Ցուցակ)
            չափ = subprocess.run(Հրահանգ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if չափ.returncode: raise 컴파일오류(չափ.stderr.decode('utf-8', 'replace'))
            return չափ_ուղի.read_text()

def Գործարկել():
    raise SystemExit(subprocess.call(['sh', str(արձակել_արմատ/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Գործարկել()
