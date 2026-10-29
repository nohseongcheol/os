#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    mapiranje_VALUE = {'out': 'KR_podaci', 'build_examples': '예제만들기', 'files': 'Datoteka_Popis', 'java': '자바실행', 'run': 'Izvrši_naredba', 'path': 'PUTANJA', 'p': 'podaci_položaj', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'LOOKUP_INDEX', 'classes': 'poduka_put', 'repo': 'spremište_put', 'root': 'korijen_adresa', 'content': 'Sadržaj_VALUE', 'source': '원본자료', 'name': 'Ime', 'target': 'cilj', 'manifest': '꾸러미명세', 'language': 'Jezik'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
