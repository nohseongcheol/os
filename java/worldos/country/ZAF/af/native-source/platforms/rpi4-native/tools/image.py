#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/Skep_foto.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('Skep_foto', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Skep_foto')
    대응 = {'total': '총량', 'start': 'Loop', 'firmware': '기초제어프로그램', 'files': 'lêer_Lys', 'archive_base': 'Argief_BASE', 'partition': 'partisie_lêer', 'archive': 'Argief', 'main': 'Loop', 'block': 'data_blokkeer', 'ROOT': 'Project_wortel', 'boot': '부팅경로', 'stage': 'toneel_VALUE', 'out': 'maatreël_data', 'expected': '예상결과', 'f': 'lêer_inskrywing', 'src': '원본주소', 'path': 'Pad', 'p': 'data_plaas', 'extracted': '추출자료', 'member': 'lid', 'mbr': '주부트기록', 'image': 'foto', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'lisensie', 'source': '원본자료', 'name': 'Naam', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'bestemming_VALUE_plaas', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
