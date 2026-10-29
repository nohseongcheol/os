#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/smíð_kerfi.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('smíð_kerfi', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('smíð_kerfi')
    vörpun_VALUE = {'network': 'Net', 'BUILD': 'smíð_slóð', 'ar': 'Safn_verkfæri', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'leturgerð_gögn', 'flags': 'afbrigði_Background_Intelligent_Transfer_Service', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'frumbreyta_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'aðferð_færsla', 'main': 'Keyra_2', 'objcopy': 'hlutur_skrá_umbreytir', 'ROOT': 'verk_rót', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'stofna_notandi_svæði', 'f': 'skrá_færsla_3d0c1245', 'extra': '추가영역', 'exports': 'flytja_út_tafla', 'jobs': '빌드작업', 'run': 'keyra_skipun', 'path': 'SLÓÐ', 'REPO': 'gagnageymsla_rót', 'tool': 'Verkfæri', 'classes': 'klasi_slóð', 'output': 'úttak_54cd5e1d', 'samples': '예제들', 'symbol': 'tákn_VALUE', 'source': '원본자료', 'name': 'Heiti', 'build_network': 'stofna_Net', 'font_info': 'leturgerð_uppl', 'manifest': 'búnt_skrá', 'work': '작업경로'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
