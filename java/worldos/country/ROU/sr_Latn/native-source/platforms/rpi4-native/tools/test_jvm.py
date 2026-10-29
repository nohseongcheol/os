#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    mapiranje_VALUE = {'message': 'obaveštavanje_SMS', 's': 'niska_podaci', 'actual': 'stvarni_KR', 'match': '일치', 'payload': 'korisni_podaci_podaci', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'koristiti', 'ROOT': 'radnja_koren', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': 'uključiti', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Dovršeno_iznos', 'classes': 'Razred_putanja', 'output': '출력결과', 'result': 'KR', 'cmd': '명령인수', 'name': 'ime', 'jar': '자바꾸러미', 'report': 'provera_valjanosti_izveštaj', 'tests': '시험목록'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
