#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. prevesti_izvor 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kompajler import greška_u_kompajliranju

radnja_koren = Path(__file__).resolve().parent

class računar_kôd_kompajler:
    def __init__(자신, 입력클래스들, 실행대상='kernel', 동적기억낱말수=262144):
        자신.putanja_Lista = [podaci.putanja for podaci in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.동적기억낱말수 = 동적기억낱말수

    def generisati(자신, stavka_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_putanja = Path(작업)/'generated.c'
            komanda = ['sh', str(radnja_koren/'미리번역.sh'), '--entry', stavka_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.동적기억낱말수), '-o', str(KR_putanja)]
            if 범용문자표기: komanda.append('--ucn')
            for Dodeli_VALUE in 내보내기목록: komanda.extend(['--export', Dodeli_VALUE])
            komanda.extend(str(putanja) for putanja in 자신.putanja_Lista)
            KR = subprocess.run(komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if KR.returncode: raise greška_u_kompajliranju(KR.stderr.decode('utf-8', 'replace'))
            return KR_putanja.read_text()

def koristiti():
    raise SystemExit(subprocess.call(['sh', str(radnja_koren/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': koristiti()
