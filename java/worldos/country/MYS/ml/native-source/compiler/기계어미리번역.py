#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. വിവർത്തനം_ചെയ്യുക_ഉറവിടം 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', സമൂഹം_പദ_ഗണനം=262144):
        자신.പാത_ലിസ്റ്റ് = [ഡാറ്റാ.വഴി for ഡാറ്റാ in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.സമൂഹം_പദ_ഗണനം = സമൂഹം_പദ_ഗണനം

    def സൃഷ്_ടിക്കുക(자신, എന്_ട്രി_പോയിന്_റ്, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            അളവ്_പാത = Path(작업)/'generated.c'
            ആജ്ഞ = ['sh', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'미리번역.sh'), '--entry', എന്_ട്രി_പോയിന്_റ്,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.സമൂഹം_പദ_ഗണനം), '-o', str(അളവ്_പാത)]
            if 범용문자표기: ആജ്ഞ.append('--ucn')
            for അസൈൻ_ചെയ്യുക_മൂല്യം in 내보내기목록: ആജ്ഞ.extend(['--export', അസൈൻ_ചെയ്യുക_മൂല്യം])
            ആജ്ഞ.extend(str(വഴി) for വഴി in 자신.പാത_ലിസ്റ്റ്)
            അളവ് = subprocess.run(ആജ്ഞ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if അളവ്.returncode: raise 컴파일오류(അളവ്.stderr.decode('utf-8', 'replace'))
            return അളവ്_പാത.read_text()

def നടപ്പിലാക്കുക():
    raise SystemExit(subprocess.call(['sh', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': നടപ്പിലാക്കുക()
