#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/uitvoer_lêer.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('uitvoer_lêer', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('uitvoer_lêer')
    대응 = {'timeout': '시간제한', 's': 'string_data', 'i': '순번', 'match': '일치', 'files': 'lêer_Lys', 'program': 'program', 'executable': '실행가능파일', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'send': 'e_pos', 'main': 'Loop', 'marker': '확인표시', 'command': 'Opdrag', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'uitvoer_bevel', 'p': 'data_plaas', 'parser': 'ontleder', 'options': 'opsies', 'kind': 'kategorie_VALUE', 'selector': 'selekteerder', 'upload_data': 'oplaai_data', 'end': 'beëindig_OFFSET', 'n': 'item_COUNT', 'd': 'bestemming_data', 'key': '누름값', 'output': '출력결과', 'line': 'lyn', 'name': 'Naam', 'upload_name': 'oplaai_naam', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
