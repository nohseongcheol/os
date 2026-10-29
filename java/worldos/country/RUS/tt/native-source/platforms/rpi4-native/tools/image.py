#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/Төзү_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('Төзү_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Төзү_IMAGE')
    대응 = {'total': '총량', 'start': 'эшләтү', 'firmware': '기초제어프로그램', 'files': 'файл_Исемлек', 'archive_base': 'Архив_BASE', 'partition': 'бүлем_файл', 'archive': 'Архив', 'main': 'эшләтү', 'block': 'мәгълүмат_тыю', 'ROOT': 'экранга_җибәрү_тамыр', 'boot': '부팅경로', 'stage': 'чор_VALUE', 'out': 'үлчәм_мәгълүмат', 'expected': '예상결과', 'f': 'файл_кертү', 'src': '원본주소', 'path': 'Yul', 'p': 'мәгълүмат_урнаштыру', 'extracted': '추출자료', 'member': 'бүлек', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': '이용허락파일', 'source': '원본자료', 'name': 'исем', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'күчерү_урыны_VALUE_урнаштыру', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
