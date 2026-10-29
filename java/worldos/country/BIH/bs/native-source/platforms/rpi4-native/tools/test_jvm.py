#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'string_podaci', 'actual': 'stvaran_mjera', 'match': '일치', 'payload': 'korisni_sadržaj_podaci', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Pokreni', 'ROOT': 'projicirati_koijen', 'text': 'Tekst', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'klasa_put', 'output': '출력결과', 'result': 'mjera', 'cmd': '명령인수', 'name': 'Naziv', 'jar': '자바꾸러미', 'report': 'provjera_izvještaj', 'tests': '시험목록'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
