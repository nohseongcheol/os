#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/Waihanga_IMAGE.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('Waihanga_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('Waihanga_IMAGE')
    대응 = {'total': '총량', 'start': 'whakahaere', 'firmware': '기초제어프로그램', 'files': 'kōnae_Rārangi', 'archive_base': 'Pūranga_BASE', 'partition': 'pātaki_kōnae', 'archive': 'Pūranga', 'main': 'whakahaere', 'block': 'raraunga_aukati', 'ROOT': 'whakaatu_pūtake', 'boot': '부팅경로', 'stage': 'atamira_uara', 'out': 'mēhua_raraunga', 'expected': '예상결과', 'f': 'kōnae_tāurunga', 'src': '원본주소', 'path': 'ara', 'p': 'raraunga_tūranga', 'extracted': '추출자료', 'member': 'mema', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'raihana', 'source': '원본자료', 'name': 'Ingoa', 'value': 'uara', 'manifest': '꾸러미명세', 'dest': 'ūnga_uara_tūranga', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
