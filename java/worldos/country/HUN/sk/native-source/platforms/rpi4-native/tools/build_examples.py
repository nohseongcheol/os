#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    mapovanie_VALUE = {'out': 'KR_údaje', 'build_examples': '예제만들기', 'files': 'Súbor_Zoznam', 'java': '자바실행', 'run': 'Vykonať_príkaz', 'path': 'Cesta', 'p': 'údaje_pozícia', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': 'inštrukcia_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'lekcia_cesta', 'repo': 'odkladací_priestor_cesta', 'root': 'koreň_adresa', 'content': 'obsah_VALUE', 'source': '원본자료', 'name': 'Názov', 'target': 'cieľová_hodnota', 'manifest': 'zväzok_manifest_zostáv', 'language': 'Jazyky'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
