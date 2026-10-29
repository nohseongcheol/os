#!/usr/bin/env python3
"""Előző_cikk Python 경로를 Java 미리 번역기에 연결한다. FORDÍTÁS_forrás 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from fordítóprogram import fordítási_hiba

teendő_gyök = Path(__file__).resolve().parent

class gép_KÓD_fordítóprogram:
    def __init__(자신, 입력클래스들, végrehajtás_cél='kernel', halommemória_szó_DARAB=262144):
        자신.útvonal_Lista = [adat.ÚTVONAL for adat in 입력클래스들]
        자신.végrehajtás_cél = végrehajtás_cél
        자신.halommemória_szó_DARAB = halommemória_szó_DARAB

    def generálás(자신, belépési_pont, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_útvonal = Path(작업)/'generated.c'
            Parancs = ['sh', str(teendő_gyök/'미리번역.sh'), '--entry', belépési_pont,
                    '--profile', 자신.végrehajtás_cél, '--heap-words', str(자신.halommemória_szó_DARAB), '-o', str(KR_útvonal)]
            if 범용문자표기: Parancs.append('--ucn')
            for átruház_ÉRTÉK in 내보내기목록: Parancs.extend(['--export', átruház_ÉRTÉK])
            Parancs.extend(str(ÚTVONAL) for ÚTVONAL in 자신.útvonal_Lista)
            KR = subprocess.run(Parancs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if KR.returncode: raise fordítási_hiba(KR.stderr.decode('utf-8', 'replace'))
            return KR_útvonal.read_text()

def Futtatás():
    raise SystemExit(subprocess.call(['sh', str(teendő_gyök/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Futtatás()
