#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/smíð_notandi_svæði.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('smíð_notandi_svæði', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('smíð_notandi_svæði')
    vörpun_VALUE = {'mode': 'aðferð_MODE', 'header': 'Haus_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Safn_verkfæri', 'posix': '포직스경로', 'payload': 'farmur_gögn', 'flags': 'afbrigði_Background_Intelligent_Transfer_Service', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'gögn', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'gagnageymsla_slóð', 'build_python': 'stofna_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Texti', 'headers': 'Haus_Listi', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'smíð', 'build_users': 'stofna_notandi_svæði', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'forrit_Haus_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'skipun_slóð', 'abi': '호출규약', 'assembly': 'samsetning', 'run': 'keyra_skipun', 'path': 'SLÓÐ', 'p': 'gögn_staða', 'changed': '바뀐자료', 'n': 'vara_COUNT', 'flag': 'Stillingar_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'klasi_slóð', 'output': 'úttak_54cd5e1d', 'loads': '적재구획', 'data_address': 'gögn_slóð', 'symbol': 'tákn_VALUE', 'root': 'rót_slóð', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Heiti', 'value': 'VALUE', 'fmt': 'snið_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
