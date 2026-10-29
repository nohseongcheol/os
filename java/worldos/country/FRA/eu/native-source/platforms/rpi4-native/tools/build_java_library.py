#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/자바라이브러리빌드.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('자바라이브러리빌드')
    대응 = {'header': 'goiburu_balio', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'karga_datuak', 'src': '원본주소', 'run': 'exekutatu_komando', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'Gela_bide_izen', 'dist': '배포경로', 'archive': 'artxibo', 'output': '출력결과', 'root': 'erro_helbide', 'name': 'Izena', 'jar': '자바꾸러미', 'b': 'SEGUNDOA_balio', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
