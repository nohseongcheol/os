#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/Create_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('Create_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Create_IMAGE')
    대응 = {'total': '총량', 'start': 'Rith_2', 'firmware': '기초제어프로그램', 'files': 'comhad_Liosta', 'archive_base': 'Cartlann_BASE', 'partition': 'deighilt_comhad', 'archive': 'Cartlann', 'main': 'Rith_2', 'block': 'sonraí_bac', 'ROOT': 'teilgean_fréamh', 'boot': '부팅경로', 'stage': 'céim_VALUE', 'out': 'tomhas_sonraí', 'expected': '예상결과', 'f': 'comhad_iontráil', 'src': '원본주소', 'path': 'CONAIR', 'p': 'sonraí_suíomh', 'extracted': '추출자료', 'member': 'ball', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ceadúnaigh', 'source': '원본자료', 'name': 'Ainm', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'sprioc_VALUE_suíomh', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
