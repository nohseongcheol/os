#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/unda_picha.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('unda_picha', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('unda_picha')
    대응 = {'total': '총량', 'start': 'endesha', 'firmware': '기초제어프로그램', 'files': 'faili_Orodha', 'archive_base': '압축기준', 'partition': 'kitenga_faili', 'archive': 'Hifadhi_eb6be19d', 'main': 'endesha', 'block': 'data_zuia', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'hatua_thamani', 'out': '결과자료', 'expected': '예상결과', 'f': 'faili_ingizo', 'src': '원본주소', 'path': 'njia', 'p': '자료위치', 'extracted': '추출자료', 'member': 'mwanachama', 'mbr': '주부트기록', 'image': 'picha', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'leseni', 'source': '원본자료', 'name': 'Jina', 'value': 'thamani', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
