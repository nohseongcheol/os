#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    mapiranje_VALUE = {'out': 'KR_podaci', 'build_examples': '예제만들기', 'files': 'Datoteka_Lista', 'java': '자바실행', 'run': 'Izvrši_komanda', 'path': 'putanja', 'p': 'podaci_pozicija', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'LOOKUP_INDEX', 'classes': 'Razred_putanja', 'repo': 'depo_putanja', 'root': 'koren_adresa', 'content': 'Sadržaj_VALUE', 'source': '원본자료', 'name': 'ime', 'target': 'cilj', 'manifest': '꾸러미명세', 'language': 'jezik'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
