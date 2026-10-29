#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    mapiranje_VALUE = {'message': 'obavijest_SMS', 's': 'niz_podaci', 'actual': 'stvaran_KR', 'match': '일치', 'payload': 'korisni_podaci_podaci', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Pokreni', 'ROOT': 'akcija_korijen', 'text': 'Tekst', 'valid': '유효함', 'includes': '포함인수', 'include': 'obuhvaćati', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Dovršeno_iznos', 'classes': 'poduka_put', 'output': '출력결과', 'result': 'REZULTAT', 'cmd': '명령인수', 'name': 'Ime', 'jar': '자바꾸러미', 'report': 'provjera_izvješće', 'tests': '시험목록'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
