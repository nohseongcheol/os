#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. Preložiť_zdroj 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kompilátor import chyba_pri_kompilácii

akcia_koreň = Path(__file__).resolve().parent

class počítač_kód_kompilátor:
    def __init__(자신, 입력클래스들, 실행대상='kernel', halda_Word_COUNT=262144):
        자신.cesta_Zoznam = [údaje.Cesta for údaje in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.halda_Word_COUNT = halda_Word_COUNT

    def generovať(자신, položka_bod, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_cesta = Path(작업)/'generated.c'
            Príkaz = ['sh', str(akcia_koreň/'미리번역.sh'), '--entry', položka_bod,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.halda_Word_COUNT), '-o', str(KR_cesta)]
            if 범용문자표기: Príkaz.append('--ucn')
            for Priradiť_VALUE in 내보내기목록: Príkaz.extend(['--export', Priradiť_VALUE])
            Príkaz.extend(str(Cesta) for Cesta in 자신.cesta_Zoznam)
            KR = subprocess.run(Príkaz, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if KR.returncode: raise chyba_pri_kompilácii(KR.stderr.decode('utf-8', 'replace'))
            return KR_cesta.read_text()

def Spustiť_2():
    raise SystemExit(subprocess.call(['sh', str(akcia_koreň/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Spustiť_2()
