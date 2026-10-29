#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/Create_image.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Create_image', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('Create_image')
    대응 = {'total': 'celkem_kapacita', 'start': 'Spustit_2', 'firmware': 'firmware_HODNOTA', 'files': 'seznam_souborů', 'archive_base': 'Archiv_BASE', 'partition': 'oddíl_Soubor', 'archive': 'Archiv', 'main': 'Spustit_2', 'block': 'datový_blok', 'ROOT': 'akce_kořen', 'boot': '부팅경로', 'stage': 'fáze_HODNOTA', 'out': 'KV_data', 'expected': '예상결과', 'f': 'Soubor_položka', 'src': '원본주소', 'path': 'cesta_2', 'p': 'data_pozice', 'extracted': '추출자료', 'member': 'člen', 'mbr': 'hlavní_spouštěcí_záznam', 'image': 'image', 'sector_count': '섹터개수', 'dist': 'distribuce_cesta', 'sha': '해시계산', 'license_': 'licence', 'source': '원본자료', 'name': 'Název', 'value': 'HODNOTA', 'manifest': 'sada_manifest', 'dest': 'cíl_HODNOTA_pozice', 'work': '작업경로'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
