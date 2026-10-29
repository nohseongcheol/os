#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/kurema_ishusho.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('kurema_ishusho', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('kurema_ishusho')
    대응 = {'total': '총량', 'start': 'ihuriro', 'firmware': '기초제어프로그램', 'files': 'dosiye_Urutonde', 'archive_base': '압축기준', 'partition': 'igice_cya_disiki_dosiye', 'archive': 'gushyingura', 'main': 'ihuriro', 'block': 'amakurushingiro_guheza', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'icyiciro_agaciro_29ee1bb7', 'out': '결과자료', 'expected': '예상결과', 'f': 'dosiye_icyinjizwa', 'src': '원본주소', 'path': 'Inzira', 'p': '자료위치', 'extracted': '추출자료', 'member': 'ugize_itsinda', 'mbr': '주부트기록', 'image': 'ishusho', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': '이용허락파일', 'source': '원본자료', 'name': 'Izina', 'value': 'agaciro', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
