#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    mapiranje_VALUE = {'out': 'KR_podaci', 'expected': '예상결과', 'phoff': 'program_Zaglavlje_pomak', 'offset': 'pomak_VALUE', 'invalid': 'nevaljan_podaci', 'path': 'PUTANJA', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'REZULTAT', 'format_': 'oblik_b87fd068', 'main': 'Pokreni', 'content': 'Sadržaj_VALUE', 'source': '원본자료', 'name': 'Ime', 'reference': 'Usporedba_polazište', 'ROOT': 'akcija_korijen', 'value': 'VALUE', 'report': 'provjera_izvješće'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
