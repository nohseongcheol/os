#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/Create_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Create_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Create_IMAGE')
    대응 = {'total': '총량', 'start': 'Pokreni', 'firmware': '기초제어프로그램', 'files': 'fajl_spisak', 'archive_base': 'Arhiva_BASE', 'partition': 'particija_fajl', 'archive': 'Arhiva', 'main': 'Pokreni', 'block': 'podaci_blokirati', 'ROOT': 'projicirati_koijen', 'boot': '부팅경로', 'stage': 'faza_VALUE', 'out': 'mjera_podaci', 'expected': '예상결과', 'f': 'fajl_unos', 'src': '원본주소', 'path': 'Putanja', 'p': 'podaci_položaj', 'extracted': '추출자료', 'member': 'član', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'licenca', 'source': '원본자료', 'name': 'Naziv', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'odredište_VALUE_položaj', 'work': '작업경로'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
