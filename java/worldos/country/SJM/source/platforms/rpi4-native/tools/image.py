#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/åpne_BILDE.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('åpne_BILDE', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('åpne_BILDE')
    tildeling_VERDI = {'total': 'total_kapasitet', 'start': 'Kjør_2', 'firmware': 'fastvare_VERDI', 'files': 'filliste', 'archive_base': 'Arkiv_grunnlag', 'partition': 'partisjon_Fil', 'archive': 'Arkiv', 'main': 'Kjør_2', 'block': 'data_blokk', 'ROOT': 'speile_rot', 'boot': '부팅경로', 'stage': 'fase_VERDI', 'out': 'KR_data', 'expected': '예상결과', 'f': 'Fil_oppføring', 'src': '원본주소', 'path': 'Sti', 'p': 'data_plassere', 'extracted': '추출자료', 'member': 'medlem', 'mbr': 'MBR', 'image': 'BILDE', 'sector_count': '섹터개수', 'dist': 'distribusjon_bane', 'sha': '해시계산', 'license_': 'lisens', 'source': '원본자료', 'name': 'Navn', 'value': 'VERDI', 'manifest': 'bunt_manifest', 'dest': 'mål_VERDI_plassere', 'work': '작업경로'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
