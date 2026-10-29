#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'mjera_podaci', 'build_examples': '예제만들기', 'files': 'fajl_spisak', 'java': '자바실행', 'run': 'Izvrši_komanda', 'path': 'Putanja', 'p': 'podaci_položaj', 'readme': 'Pročitaj_me', 'build_java_library': '자바라이브러리만들기', 'code': 'programska_naredba_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'klasa_put', 'repo': '저장소경로', 'root': 'koijen_adresa', 'content': 'Sadržaj_VALUE', 'source': '원본자료', 'name': 'Naziv', 'target': 'cilj', 'manifest': '꾸러미명세', 'language': 'Jezik'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
