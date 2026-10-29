#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바라이브러리빌드')
    mapovanie_VALUE = {'header': 'Nadpis_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'Systémové_informácie', 'payload': 'údajová_časť_údaje', 'src': '원본주소', 'run': 'Vykonať_príkaz', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'lekcia_cesta', 'dist': '배포경로', 'archive': 'Archív', 'output': '출력결과', 'root': 'koreň_adresa', 'name': 'Názov', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
