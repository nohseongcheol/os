#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Tekki_Cosaan 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 컴파일러 import 컴파일오류

기준 = Path(__file__).resolve().parent

class 기계어번역기:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.Yoonu_jëmale_lim = [mbir.Yoonu_jëmale for mbir in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def 생성(자신, dugal_xabaar_Tomb, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            결과경로 = Path(작업)/'generated.c'
            ndigel = ['sh', str(기준/'미리번역.sh'), '--entry', dugal_xabaar_Tomb,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(결과경로)]
            if 범용문자표기: ndigel.append('--ucn')
            for 지정 in 내보내기목록: ndigel.extend(['--export', 지정])
            ndigel.extend(str(Yoonu_jëmale) for Yoonu_jëmale in 자신.Yoonu_jëmale_lim)
            결과 = subprocess.run(ndigel, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if 결과.returncode: raise 컴파일오류(결과.stderr.decode('utf-8', 'replace'))
            return 결과경로.read_text()

def daw():
    raise SystemExit(subprocess.call(['sh', str(기준/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': daw()
