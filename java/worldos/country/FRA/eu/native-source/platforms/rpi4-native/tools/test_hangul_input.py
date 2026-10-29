#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/한글입력시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('한글입력시험')
    대응 = {'expected': '예상결과', 'Keyboard': 'teklatu', 'press': 'sakatu_gako', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_붙이기유니코드', 'data': 'datuak', 'key': '누름값', 'send': 'bidali', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'ikur_balio', 'char': 'karaktere_datuak', 'type': 'MOTA_Kategoria'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
