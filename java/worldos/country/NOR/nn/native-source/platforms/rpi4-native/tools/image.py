#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/Opprett_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('Opprett_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Opprett_IMAGE')
    대응 = {'total': '총량', 'start': 'Køyr_2', 'firmware': '기초제어프로그램', 'files': 'fil_Liste', 'archive_base': 'Arkiv_BASE', 'partition': 'partisjon_fil', 'archive': 'Arkiv', 'main': 'Køyr_2', 'block': 'data_Blokker', 'ROOT': 'spegle_rot', 'boot': '부팅경로', 'stage': 'stadium_VALUE', 'out': 'forretningsmål_data', 'expected': '예상결과', 'f': 'fil_oppføring', 'src': '원본주소', 'path': 'STIGE', 'p': 'data_plassere', 'extracted': '추출자료', 'member': 'medlem', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'lisens', 'source': '원본자료', 'name': 'Namn', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'mål_VALUE_plassere', 'work': '작업경로'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
