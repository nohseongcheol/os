#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/Create_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Create_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Create_IMAGE')
    mapiranje_VALUE = {'total': 'ukupni_zbroj_kapacitet', 'start': 'Pokreni', 'firmware': 'oprema_VALUE', 'files': 'Datoteka_Popis', 'archive_base': 'Arhiva_BASE', 'partition': 'particija_Datoteka', 'archive': 'Arhiva', 'main': 'Pokreni', 'block': 'podatkovni_blok', 'ROOT': 'akcija_korijen', 'boot': '부팅경로', 'stage': 'faza_VALUE', 'out': 'KR_podaci', 'expected': '예상결과', 'f': 'Datoteka_unos', 'src': '원본주소', 'path': 'PUTANJA', 'p': 'podaci_položaj', 'extracted': '추출자료', 'member': 'član', 'mbr': 'MBR', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'licenca', 'source': '원본자료', 'name': 'Ime', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'odredište_VALUE_položaj', 'work': '작업경로'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
