#!/usr/bin/env python3
"""Anteriorul_element Python 경로를 Java 미리 번역기에 연결한다. TRANSLATE_sursă 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from compilator import eroare_la_compilare

Project_rădăcină = Path(__file__).resolve().parent

class mașină_cod_compilator:
    def __init__(자신, 입력클래스들, executare_țintă='kernel', 동적기억낱말수=262144):
        자신.cale_Listă = [date.Cale for date in 입력클래스들]
        자신.executare_țintă = executare_țintă
        자신.동적기억낱말수 = 동적기억낱말수

    def genera(자신, intrare_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_cale = Path(작업)/'generated.c'
            Comandă = ['sh', str(Project_rădăcină/'미리번역.sh'), '--entry', intrare_p,
                    '--profile', 자신.executare_țintă, '--heap-words', str(자신.동적기억낱말수), '-o', str(KR_cale)]
            if 범용문자표기: Comandă.append('--ucn')
            for atribui_VALUE in 내보내기목록: Comandă.extend(['--export', atribui_VALUE])
            Comandă.extend(str(Cale) for Cale in 자신.cale_Listă)
            KR = subprocess.run(Comandă, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if KR.returncode: raise eroare_la_compilare(KR.stderr.decode('utf-8', 'replace'))
            return KR_cale.read_text()

def Pornește():
    raise SystemExit(subprocess.call(['sh', str(Project_rădăcină/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Pornește()
