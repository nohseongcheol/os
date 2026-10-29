#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/test_virtuálny_počítač_Java.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('test_virtuálny_počítač_Java', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('test_virtuálny_počítač_Java')
    mapovanie_VALUE = {'message': 'upozornenie_SMS', 's': 'reťazec_údaje', 'actual': 'skutočný_KR', 'match': '일치', 'payload': 'údajová_časť_údaje', 'cases': 'test_prípad', 'fixture': 'test_údaje', 'main': 'Spustiť_2', 'ROOT': 'akcia_koreň', 'text': 'Spracovanie_textu', 'valid': '유효함', 'includes': '포함인수', 'include': 'zahrnúť', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Dokončené_úlohy_suma', 'classes': 'lekcia_cesta', 'output': '출력결과', 'result': 'KR', 'cmd': '명령인수', 'name': 'Názov', 'jar': '자바꾸러미', 'report': 'overenie_správa', 'tests': 'test_Zoznam'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
