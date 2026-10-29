#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    kartēšana_VALUE = {'message': 'informēšana_SMS', 's': 'virkne_dati', 'actual': 'faktisks_mērs', 'match': '일치', 'payload': 'vērtums_dati', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Palaist', 'ROOT': 'Project_sakne', 'text': 'Teksts', 'valid': '유효함', 'includes': '포함인수', 'include': 'iekļaut', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Pabeigti_summa', 'classes': 'klase_ceļš', 'output': 'ražojums', 'result': 'mērs', 'cmd': '명령인수', 'name': 'Nosaukums', 'jar': '자바꾸러미', 'report': 'validācija_ziņot', 'tests': '시험목록'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
