#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/ħalaq_IMAGE.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('ħalaq_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ħalaq_IMAGE')
    대응 = {'total': '총량', 'start': 'serje', 'firmware': '기초제어프로그램', 'files': 'fajl_Lista', 'archive_base': 'Arkivju_BASE', 'partition': 'taqsima_fajl', 'archive': 'Arkivju', 'main': 'serje', 'block': 'data_imblokka', 'ROOT': 'pprojetta_għerq', 'boot': '부팅경로', 'stage': 'palk_VALUE', 'out': 'miżura_data', 'expected': '예상결과', 'f': 'fajl_entrata', 'src': '원본주소', 'path': 'mogħdija', 'p': 'data_pożizzjoni', 'extracted': '추출자료', 'member': 'membru', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'i_lliċenzja', 'source': '원본자료', 'name': 'isem', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'destinazzjoni_VALUE_pożizzjoni', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
