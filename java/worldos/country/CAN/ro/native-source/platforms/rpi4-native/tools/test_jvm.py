#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    mapare_VALUE = {'message': 'înștiințare_SMS', 's': 'șir_date', 'actual': 'real_KR', 'match': '일치', 'payload': 'sarcină_date', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Pornește', 'ROOT': 'Project_rădăcină', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': 'include', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Finalizate_sumă', 'classes': 'Clasă_cale', 'output': '출력결과', 'result': 'KR', 'cmd': '명령인수', 'name': 'Nume', 'jar': '자바꾸러미', 'report': 'validare_raport', 'tests': '시험목록'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
