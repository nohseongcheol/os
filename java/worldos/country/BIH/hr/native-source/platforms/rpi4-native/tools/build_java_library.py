#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바라이브러리빌드')
    mapiranje_VALUE = {'header': 'Zaglavlje_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'Podaci_o_sustavu', 'payload': 'korisni_podaci_podaci', 'src': '원본주소', 'run': 'Izvrši_naredba', 'build_java_library': '자바라이브러리만들기', 'relative': 'relativni_put', 'classes': 'poduka_put', 'dist': '배포경로', 'archive': 'Arhiva', 'output': '출력결과', 'root': 'korijen_adresa', 'name': 'Ime', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
