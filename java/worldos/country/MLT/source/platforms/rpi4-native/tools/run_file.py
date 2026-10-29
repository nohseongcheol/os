#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/eżegwixxa_fajl.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('eżegwixxa_fajl', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('eżegwixxa_fajl')
    대응 = {'timeout': '시간제한', 's': 'string_data', 'i': '순번', 'match': '일치', 'files': 'fajl_Lista', 'program': 'programm', 'executable': '실행가능파일', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proċess', 'send': 'bagħat', 'main': 'serje', 'marker': '확인표시', 'command': 'kmand', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'eżegwixxa_kmand', 'p': 'data_pożizzjoni', 'parser': '인수해석기', 'options': 'Għażliet', 'kind': 'kategorija_VALUE', 'selector': 'selettur', 'upload_data': 'tella_data', 'end': 'ttermina_OFFSET', 'n': 'element_COUNT', 'd': 'destinazzjoni_data', 'key': '누름값', 'output': '출력결과', 'line': 'linja', 'name': 'isem', 'upload_name': 'tella_isem', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
