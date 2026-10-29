#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/kawe_kōnae.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('kawe_kōnae', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('kawe_kōnae')
    대응 = {'timeout': '시간제한', 's': 'aho_raraunga', 'i': '순번', 'match': '일치', 'files': 'kōnae_Rārangi', 'program': 'kaupapa', 'executable': '실행가능파일', 'args': 'tohenga_HUĀNGA', 'chunk': '조각', 'data': 'raraunga', 'proc': 'Hātepe', 'send': 'tuku', 'main': 'whakahaere', 'marker': '확인표시', 'command': 'tono', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'kawe_tono', 'p': 'raraunga_tūranga', 'parser': '인수해석기', 'options': 'Kōwhiringa', 'kind': 'kāwai_uara', 'selector': 'pūtīpako', 'upload_data': 'tukuatu_raraunga', 'end': 'mutu_OFFSET', 'n': 'tuemi_COUNT', 'd': 'ūnga_raraunga', 'key': '누름값', 'output': '출력결과', 'line': 'hononga', 'name': 'Ingoa', 'upload_name': 'tukuatu_ingoa', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
