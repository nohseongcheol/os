#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    kartēšana_VALUE = {'out': 'mērs_dati', 'build_examples': '예제만들기', 'files': 'Fails_Saraksts', 'java': '자바실행', 'run': 'Izpildīt_komanda', 'path': 'CEĻŠ', 'p': 'dati_amats', 'readme': 'fails_Lasi_mani', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'LOOKUP_INDEX', 'classes': 'klase_ceļš', 'repo': 'repozitorijs_ceļš', 'root': 'sakne_adrese', 'content': 'Saturs_VALUE', 'source': '원본자료', 'name': 'Nosaukums', 'target': 'mērķis', 'manifest': '꾸러미명세', 'language': 'Valodas'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
