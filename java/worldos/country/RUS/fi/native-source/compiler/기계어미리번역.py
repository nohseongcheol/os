#!/usr/bin/env python3
"""Edellinen_kohde Python 경로를 Java 미리 번역기에 연결한다. KÄÄNNÄ_lähde 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kääntäjä import 컴파일오류

aloite_juuri = Path(__file__).resolve().parent

class kone_KOODI_kääntäjä:
    def __init__(자신, 입력클래스들, suoritus_kohde='kernel', keko_Word_LASKE=262144):
        자신.polku_luettelo = [data.polku_2 for data in 입력클래스들]
        자신.suoritus_kohde = suoritus_kohde
        자신.keko_Word_LASKE = keko_Word_LASKE

    def generoida(자신, aloituskohta, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_polku = Path(작업)/'generated.c'
            komento = ['sh', str(aloite_juuri/'미리번역.sh'), '--entry', aloituskohta,
                    '--profile', 자신.suoritus_kohde, '--heap-words', str(자신.keko_Word_LASKE), '-o', str(KR_polku)]
            if 범용문자표기: komento.append('--ucn')
            for Määritä_ARVO in 내보내기목록: komento.extend(['--export', Määritä_ARVO])
            komento.extend(str(polku_2) for polku_2 in 자신.polku_luettelo)
            TULOS = subprocess.run(komento, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if TULOS.returncode: raise 컴파일오류(TULOS.stderr.decode('utf-8', 'replace'))
            return KR_polku.read_text()

def Suorita_2():
    raise SystemExit(subprocess.call(['sh', str(aloite_juuri/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Suorita_2()
