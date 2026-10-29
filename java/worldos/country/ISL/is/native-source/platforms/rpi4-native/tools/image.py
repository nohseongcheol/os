#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/stofna_mynd.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('stofna_mynd', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('stofna_mynd')
    vörpun_VALUE = {'total': 'samtala_afkastageta', 'start': 'Keyra_2', 'firmware': '기초제어프로그램', 'files': 'skrá_Listi', 'archive_base': 'Safn_BASE', 'partition': 'sneið_skrá', 'archive': 'Safn', 'main': 'Keyra_2', 'block': 'gögn_útiloka', 'ROOT': 'verk_rót', 'boot': '부팅경로', 'stage': 'stig_VALUE', 'out': 'mæld_stærð_gögn', 'expected': '예상결과', 'f': 'skrá_færsla_3d0c1245', 'src': '원본주소', 'path': 'SLÓÐ', 'p': 'gögn_staða', 'extracted': '추출자료', 'member': 'aðili', 'mbr': '주부트기록', 'image': 'mynd', 'sector_count': '섹터개수', 'dist': 'dreifing_slóð', 'sha': '해시계산', 'license_': 'leyfi', 'source': '원본자료', 'name': 'Heiti', 'value': 'VALUE', 'manifest': 'búnt_skrá', 'dest': 'endastaður_VALUE_staða', 'work': '작업경로'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
