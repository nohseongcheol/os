#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/bou_stelsel.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('bou_stelsel', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bou_stelsel')
    대응 = {'network': 'Netwerk', 'BUILD': 'bou_pad', 'ar': 'Argief_nutsmiddel', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_data', 'flags': 'konfigurasie_Agtergrond_intelligente_oordragdiens', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metode_inskrywing', 'main': 'Loop', 'objcopy': 'objek_lêer_omsetter', 'ROOT': 'Project_wortel', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Skep_gebruiker_ruimte', 'f': 'lêer_inskrywing', 'extra': '추가영역', 'exports': 'uitvoer_tabel', 'jobs': '빌드작업', 'run': 'uitvoer_bevel', 'path': 'Pad', 'REPO': 'bewaarplek_wortel', 'tool': 'Nutsmiddels', 'classes': 'Klas_pad', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbool_VALUE', 'source': '원본자료', 'name': 'Naam', 'build_network': 'Skep_Netwerk', 'font_info': 'font_inligting', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
