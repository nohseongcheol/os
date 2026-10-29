#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/Create_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('Create_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Create_IMAGE')
    대응 = {'total': '총량', 'start': 'Изврши_2', 'firmware': '기초제어프로그램', 'files': 'датотека_Список', 'archive_base': 'Архива_BASE', 'partition': 'партиција_датотека', 'archive': 'Архива', 'main': 'Изврши_2', 'block': 'податоци_блокирај', 'ROOT': 'Project_корен', 'boot': '부팅경로', 'stage': 'фаза_VALUE', 'out': 'мерка_податоци', 'expected': '예상결과', 'f': 'датотека_внес', 'src': '원본주소', 'path': 'ПАТЕКА', 'p': 'податоци_позиционирање', 'extracted': '추출자료', 'member': 'член', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'лиценцира', 'source': '원본자료', 'name': 'Име', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'одредиште_VALUE_позиционирање', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
