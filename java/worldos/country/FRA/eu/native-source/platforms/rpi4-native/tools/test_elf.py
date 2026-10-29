#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/실행파일시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('실행파일시험')
    대응 = {'out': 'neurria_datuak', 'expected': '예상결과', 'phoff': 'aplik_goiburu_Geruzak', 'offset': 'Geruzak_balio', 'invalid': 'baliogabe_datuak', 'path': 'Bide_izena', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'EMAITZA', 'format_': 'formatu_b87fd068', 'main': 'Exekutatu_2', 'content': 'eduki_balio', 'source': '원본자료', 'name': 'Izena', 'reference': 'Konparazioa_oinarri', 'ROOT': 'Project_erro', 'value': 'balio', 'report': 'balidazio_txosten'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
