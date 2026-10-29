#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/tlhama_Setshwantsho.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('tlhama_Setshwantsho', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('tlhama_Setshwantsho')
    대응 = {'total': '총량', 'start': 'dirisa', 'firmware': '기초제어프로그램', 'files': 'faele_lenaane', 'archive_base': '압축기준', 'partition': 'karoganyo_faele', 'archive': 'boloka', 'main': 'dirisa', 'block': 'tshedimosetso_thibela', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'logato_Boleng', 'out': '결과자료', 'expected': '예상결과', 'f': 'faele_tsenyo', 'src': '원본주소', 'path': 'tsela', 'p': '자료위치', 'extracted': '추출자료', 'member': 'karolo', 'mbr': '주부트기록', 'image': 'Setshwantsho', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'Laesense', 'source': '원본자료', 'name': 'leina', 'value': 'Boleng', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
