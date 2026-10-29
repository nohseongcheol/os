#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/yarat_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('yarat_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('yarat_IMAGE')
    대응 = {'total': '총량', 'start': 'İcra_Et', 'firmware': '기초제어프로그램', 'files': 'fayl_Siyahı', 'archive_base': 'Arxiv_BASE', 'partition': 'bölmə_fayl', 'archive': 'Arxiv', 'main': 'İcra_Et', 'block': 'verilənlər_blokla', 'ROOT': 'Project_kök', 'boot': '부팅경로', 'stage': 'səhnə_VALUE', 'out': 'ölçü_verilənlər', 'expected': '예상결과', 'f': 'fayl_daxiletmə', 'src': '원본주소', 'path': 'Cığır', 'p': 'verilənlər_yerinə_qoymaq', 'extracted': '추출자료', 'member': 'üzv', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'lisenziya', 'source': '원본자료', 'name': 'Ad', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'təyinat_VALUE_yerinə_qoymaq', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
