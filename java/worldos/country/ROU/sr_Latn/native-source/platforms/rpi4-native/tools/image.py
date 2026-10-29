#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/Create_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Create_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Create_IMAGE')
    mapiranje_VALUE = {'total': 'ukupan_kapacitet', 'start': 'koristiti', 'firmware': 'firmver_VALUE', 'files': 'Datoteka_Lista', 'archive_base': 'Arhiva_BASE', 'partition': 'particija_Datoteka', 'archive': 'Arhiva', 'main': 'koristiti', 'block': 'blok_podataka', 'ROOT': 'radnja_koren', 'boot': '부팅경로', 'stage': 'faza_VALUE', 'out': 'KR_podaci', 'expected': '예상결과', 'f': 'Datoteka_stavka', 'src': '원본주소', 'path': 'putanja', 'p': 'podaci_pozicija', 'extracted': '추출자료', 'member': 'član', 'mbr': 'MBR', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'licenca', 'source': '원본자료', 'name': 'ime', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'odredište_VALUE_pozicija', 'work': '작업경로'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
