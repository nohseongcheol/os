#!/usr/bin/env python3
"""Předchozí_zboží Python 경로를 Java 미리 번역기에 연결한다. převést_zdroj 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kompilátor import chyba_kompilace

akce_kořen = Path(__file__).resolve().parent

class počítač_KÓD_kompilátor:
    def __init__(자신, 입력클래스들, spuštění_cíl='kernel', halda_počet_slov=262144):
        자신.cesta_Seznam = [data.cesta_2 for data in 입력클래스들]
        자신.spuštění_cíl = spuštění_cíl
        자신.halda_počet_slov = halda_počet_slov

    def generovat(자신, vstupní_bod, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KV_cesta = Path(작업)/'generated.c'
            příkaz = ['sh', str(akce_kořen/'미리번역.sh'), '--entry', vstupní_bod,
                    '--profile', 자신.spuštění_cíl, '--heap-words', str(자신.halda_počet_slov), '-o', str(KV_cesta)]
            if 범용문자표기: příkaz.append('--ucn')
            for Přiřadit_HODNOTA in 내보내기목록: příkaz.extend(['--export', Přiřadit_HODNOTA])
            příkaz.extend(str(cesta_2) for cesta_2 in 자신.cesta_Seznam)
            VÝSLEDEK = subprocess.run(příkaz, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if VÝSLEDEK.returncode: raise chyba_kompilace(VÝSLEDEK.stderr.decode('utf-8', 'replace'))
            return KV_cesta.read_text()

def Spustit_2():
    raise SystemExit(subprocess.call(['sh', str(akce_kořen/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Spustit_2()
