#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/영상만들기.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('영상만들기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('영상만들기')
    대응 = {'total': '총량', 'start': 'Diriša', 'firmware': '기초제어프로그램', 'files': 'faele_Lenaneo', 'archive_base': '압축기준', 'partition': 'karolo_ya_tisiki_faele', 'archive': 'Akhaebe', 'main': 'Diriša', 'block': 'data_thibela', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'karolo_boleng_29ee1bb7', 'out': '결과자료', 'expected': '예상결과', 'f': 'faele_go_tsenya_tshedimošo', 'src': '원본주소', 'path': 'Tsejana', 'p': '자료위치', 'extracted': '추출자료', 'member': 'setho', 'mbr': '주부트기록', 'image': 'seswantšho', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'laesentshe', 'source': '원본자료', 'name': 'Leina', 'value': 'boleng', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
