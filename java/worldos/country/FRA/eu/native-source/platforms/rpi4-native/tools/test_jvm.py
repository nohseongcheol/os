#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/자바가상기계시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'kate_datuak', 'actual': 'benetako_neurria', 'match': '일치', 'payload': 'karga_datuak', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Exekutatu_2', 'ROOT': 'Project_erro', 'text': 'Testua', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Osatutakoak_kopuru', 'classes': 'Gela_bide_izen', 'output': '출력결과', 'result': 'EMAITZA', 'cmd': '명령인수', 'name': 'Izena', 'jar': '자바꾸러미', 'report': 'balidazio_txosten', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
