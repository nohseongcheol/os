#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/Krijo_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('Krijo_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Krijo_IMAGE')
    대응 = {'total': '총량', 'start': 'Ekzekuto', 'firmware': '기초제어프로그램', 'files': 'skedar_Listë', 'archive_base': 'arkiv_BASE', 'partition': 'ndarje_skedar', 'archive': 'arkiv', 'main': 'Ekzekuto', 'block': 'të_dhëna_bllokoj', 'ROOT': 'Project_rrënjë', 'boot': '부팅경로', 'stage': 'fazë_VALUE', 'out': 'llogaritje_të_dhëna', 'expected': '예상결과', 'f': 'skedar_futje', 'src': '원본주소', 'path': 'POZICIONI', 'p': 'të_dhëna_pozicioni', 'extracted': '추출자료', 'member': 'anëtar', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'licencoj', 'source': '원본자료', 'name': 'Emër', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'vendmbërritje_VALUE_pozicioni', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
