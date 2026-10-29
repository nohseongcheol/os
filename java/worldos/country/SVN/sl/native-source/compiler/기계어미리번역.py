#!/usr/bin/env python3
"""이전 Python 경로를 Java 미리 번역기에 연결한다. prevesti_vir 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from prevajalnik import napaka_pri_prevajanju

pobuda_koren = Path(__file__).resolve().parent

class računalnik_CODE_prevajalnik:
    def __init__(자신, 입력클래스들, 실행대상='kernel', kopica_Word_COUNT=262144):
        자신.pot_Seznam = [podatki.POT for podatki in 입력클래스들]
        자신.실행대상 = 실행대상
        자신.kopica_Word_COUNT = kopica_Word_COUNT

    def ustvariti(자신, vnos_p, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_pot = Path(작업)/'generated.c'
            Ukaz = ['sh', str(pobuda_koren/'미리번역.sh'), '--entry', vnos_p,
                    '--profile', 자신.실행대상, '--heap-words', str(자신.kopica_Word_COUNT), '-o', str(KR_pot)]
            if 범용문자표기: Ukaz.append('--ucn')
            for Dodeli_VALUE in 내보내기목록: Ukaz.extend(['--export', Dodeli_VALUE])
            Ukaz.extend(str(POT) for POT in 자신.pot_Seznam)
            REZULTAT = subprocess.run(Ukaz, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if REZULTAT.returncode: raise napaka_pri_prevajanju(REZULTAT.stderr.decode('utf-8', 'replace'))
            return KR_pot.read_text()

def Zaženi():
    raise SystemExit(subprocess.call(['sh', str(pobuda_koren/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Zaženi()
