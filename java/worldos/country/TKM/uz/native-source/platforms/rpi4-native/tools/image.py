#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/Yaratish_rasm.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('Yaratish_rasm', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Yaratish_rasm')
    대응 = {'total': '총량', 'start': 'Bajarish', 'firmware': '기초제어프로그램', 'files': 'fayl_Ro_yxat', 'archive_base': 'Arxiv_BASE', 'partition': 'bo_lim_fayl', 'archive': 'Arxiv', 'main': 'Bajarish', 'block': 'ma_lumotlar_bloklash', 'ROOT': 'Project_ildiz', 'boot': '부팅경로', 'stage': 'bosqich_VALUE', 'out': 'o_lchov_ma_lumotlar', 'expected': '예상결과', 'f': 'fayl_kiritish', 'src': '원본주소', 'path': 'yo_l', 'p': 'ma_lumotlar_holat', 'extracted': '추출자료', 'member': 'a_zo', 'mbr': '주부트기록', 'image': 'rasm', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': '이용허락파일', 'source': '원본자료', 'name': 'Nomi', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'ko_chirish_joyi_VALUE_holat', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
