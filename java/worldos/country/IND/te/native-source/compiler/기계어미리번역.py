#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. అనువదించు_మూలం 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.పథం_జాబితా = [డేటా.పాత్ for డేటా in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def రూపొందించు(자신, ప్రవేశం_పాయింట్, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            ప్రమాణం_పథం = Path(작업)/'generated.c'
            ఆదేశము = ['sh', str(ప్రొజెక్ట్_మూలం/'미리번역.sh'), '--entry', ప్రవేశం_పాయింట్,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(ప్రమాణం_పథం)]
            if 범용문자표기: ఆదేశము.append('--ucn')
            for కేటాయించు_మూల్యం in 내보내기목록: ఆదేశము.extend(['--export', కేటాయించు_మూల్యం])
            ఆదేశము.extend(str(పాత్) for పాత్ in 자신.పథం_జాబితా)
            ప్రమాణం = subprocess.run(ఆదేశము, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ప్రమాణం.returncode: raise 컴파일오류(ప్రమాణం.stderr.decode('utf-8', 'replace'))
            return ప్రమాణం_పథం.read_text()

def నడుపుము():
    raise SystemExit(subprocess.call(['sh', str(ప్రొజెక్ట్_మూలం/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': నడుపుము()
