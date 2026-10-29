#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/bou_gebruiker_ruimte.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('bou_gebruiker_ruimte', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bou_gebruiker_ruimte')
    대응 = {'mode': 'metode_MODE', 'header': 'Loopkop_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Argief_nutsmiddel', 'posix': '포직스경로', 'payload': 'lading_data', 'flags': 'konfigurasie_Agtergrond_intelligente_oordragdiens', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'bewaarplek_pad', 'build_python': 'Skep_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Teks', 'headers': 'Loopkop_Lys', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'bou', 'build_users': 'Skep_gebruiker_ruimte', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'program_Loopkop_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'bevel_adres', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'uitvoer_bevel', 'path': 'Pad', 'p': 'data_plaas', 'changed': '바뀐자료', 'n': 'item_COUNT', 'flag': 'Instellings_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'Klas_pad', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'data_adres', 'symbol': 'simbool_VALUE', 'root': 'wortel_adres', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Naam', 'value': 'VALUE', 'fmt': 'formaat_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
