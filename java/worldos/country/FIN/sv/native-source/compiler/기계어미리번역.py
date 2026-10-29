#!/usr/bin/env python3
"""Föregående_objekt Python 경로를 Java 미리 번역기에 연결한다. ÖVERSÄTT_källa 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kompilerare import kompileringsfel

åtgärd_rot = Path(__file__).resolve().parent

class dator_KOD_kompilerare:
    def __init__(자신, 입력클래스들, körning_mål='kernel', heap_Ord_ANTAL=262144):
        자신.väg_ange = [data.sökväg_2 for data in 입력클래스들]
        자신.körning_mål = körning_mål
        자신.heap_Ord_ANTAL = heap_Ord_ANTAL

    def generera(자신, startpunkt, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_väg = Path(작업)/'generated.c'
            kommando = ['sh', str(åtgärd_rot/'미리번역.sh'), '--entry', startpunkt,
                    '--profile', 자신.körning_mål, '--heap-words', str(자신.heap_Ord_ANTAL), '-o', str(KR_väg)]
            if 범용문자표기: kommando.append('--ucn')
            for Tilldela_värde in 내보내기목록: kommando.extend(['--export', Tilldela_värde])
            kommando.extend(str(sökväg_2) for sökväg_2 in 자신.väg_ange)
            RESULTAT = subprocess.run(kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if RESULTAT.returncode: raise kompileringsfel(RESULTAT.stderr.decode('utf-8', 'replace'))
            return KR_väg.read_text()

def Kör():
    raise SystemExit(subprocess.call(['sh', str(åtgärd_rot/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Kör()
