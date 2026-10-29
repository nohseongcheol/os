#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/sortu_irudi.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('sortu_irudi', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('sortu_irudi')
    대응 = {'total': '총량', 'start': 'Exekutatu_2', 'firmware': '기초제어프로그램', 'files': 'fitxategi_Zerrenda', 'archive_base': 'artxibo_BASE', 'partition': 'partizio_fitxategi', 'archive': 'artxibo', 'main': 'Exekutatu_2', 'block': 'datuak_blokeatu', 'ROOT': 'Project_erro', 'boot': '부팅경로', 'stage': 'fase_balio', 'out': 'neurria_datuak', 'expected': '예상결과', 'f': 'fitxategi_sarrera', 'src': '원본주소', 'path': 'Bide_izena', 'p': 'datuak_kargu', 'extracted': '추출자료', 'member': 'kide', 'mbr': '주부트기록', 'image': 'irudi', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'lizentzia_eman', 'source': '원본자료', 'name': 'Izena', 'value': 'balio', 'manifest': '꾸러미명세', 'dest': 'helburu_balio_kargu', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
