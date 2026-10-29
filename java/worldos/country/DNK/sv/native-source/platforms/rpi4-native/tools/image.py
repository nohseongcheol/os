#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/Skapa_BILD.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('Skapa_BILD', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('Skapa_BILD')
    mappning_värde = {'total': 'summa_kapacitet', 'start': 'Kör', 'firmware': 'inbyggd_programvara_värde', 'files': 'fillista', 'archive_base': 'Arkiv_BAS', 'partition': 'partition_fil', 'archive': 'Arkiv', 'main': 'Kör', 'block': 'datablock', 'ROOT': 'åtgärd_rot', 'boot': '부팅경로', 'stage': 'scen_värde', 'out': 'KR_data', 'expected': '예상결과', 'f': 'fil_post', 'src': '원본주소', 'path': 'sökväg_2', 'p': 'data_placera', 'extracted': '추출자료', 'member': 'medlem', 'mbr': 'huvudstartpost', 'image': 'BILD', 'sector_count': '섹터개수', 'dist': 'fördelning_väg', 'sha': '해시계산', 'license_': 'licens', 'source': '원본자료', 'name': 'Namn', 'value': 'värde', 'manifest': 'bunt_manifest', 'dest': 'mål_värde_placera', 'work': '작업경로'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
