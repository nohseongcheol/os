#!/usr/bin/env python3
"""Wstecz_towar Python 경로를 Java 미리 번역기에 연결한다. TŁUMACZ_źródło 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from kompilator import błąd_kompilacji

Project_korzeń = Path(__file__).resolve().parent

class maszyna_KOD_kompilator:
    def __init__(자신, 입력클래스들, wykonanie_cel='kernel', sterta_Word_ILE_LICZB=262144):
        자신.ścieżka_Lista = [dane.ścieżka_2 for dane in 입력클래스들]
        자신.wykonanie_cel = wykonanie_cel
        자신.sterta_Word_ILE_LICZB = sterta_Word_ILE_LICZB

    def generować(자신, punkt_wejścia, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_ścieżka = Path(작업)/'generated.c'
            polecenie = ['sh', str(Project_korzeń/'미리번역.sh'), '--entry', punkt_wejścia,
                    '--profile', 자신.wykonanie_cel, '--heap-words', str(자신.sterta_Word_ILE_LICZB), '-o', str(KR_ścieżka)]
            if 범용문자표기: polecenie.append('--ucn')
            for Przypisz_WARTOŚĆ in 내보내기목록: polecenie.extend(['--export', Przypisz_WARTOŚĆ])
            polecenie.extend(str(ścieżka_2) for ścieżka_2 in 자신.ścieżka_Lista)
            WYNIK = subprocess.run(polecenie, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if WYNIK.returncode: raise błąd_kompilacji(WYNIK.stderr.decode('utf-8', 'replace'))
            return KR_ścieżka.read_text()

def Uruchom_2():
    raise SystemExit(subprocess.call(['sh', str(Project_korzeń/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': Uruchom_2()
