#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/예제빌드.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('예제빌드')
    대응 = {'out': 'neurria_datuak', 'build_examples': '예제만들기', 'files': 'fitxategi_Zerrenda', 'java': '자바실행', 'run': 'exekutatu_komando', 'path': 'Bide_izena', 'p': 'datuak_kargu', 'readme': 'IRAKHAU', 'build_java_library': '자바라이브러리만들기', 'code': 'instrukzio_SEKUENTZIA', 'index': 'BEGIRATU_INDIZE', 'classes': 'Gela_bide_izen', 'repo': 'biltegi_bide_izen', 'root': 'erro_helbide', 'content': 'eduki_balio', 'source': '원본자료', 'name': 'Izena', 'target': 'helburu_balio', 'manifest': '꾸러미명세', 'language': 'Hizkuntza'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
