#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/개발꾸러미내보내기.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('개발꾸러미내보내기')
    대응 = {'out': 'neurria_datuak', 'obj': 'helburuko_fitxategi', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'artxibo', 'main': 'Exekutatu_2', 'posix': '포직스경로', 'files': 'fitxategi_Zerrenda', 'source': '원본자료', 'name': 'Izena', 'target': 'helburu_balio', 'ROOT': 'Project_erro', 'destination': 'helburu_datuak_helbide', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
