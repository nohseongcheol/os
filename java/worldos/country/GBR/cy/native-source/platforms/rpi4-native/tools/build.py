#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/llunio_system.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('llunio_system', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('llunio_system')
    대응 = {'network': 'Rhwydwaith', 'BUILD': 'llunio_llwybr', 'ar': 'Archif_offeryn', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ffont_data', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'arg_ARAE', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'dull_cofnod', 'main': 'Gweithredu_2', 'objcopy': 'gwrthrych_ffeil_trawsnewidydd', 'ROOT': 'prosiect_gwraidd', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Creu_defnyddiwr_lle', 'f': 'ffeil_cofnod', 'extra': '추가영역', 'exports': 'allgludo_tabl', 'jobs': '빌드작업', 'run': 'Gweithredu_gorchymyn', 'path': 'LLWYBR', 'REPO': '저장소', 'tool': 'Offer', 'classes': 'Dosbarth_llwybr', 'output': '출력결과', 'samples': '예제들', 'symbol': 'symbol_VALUE', 'source': '원본자료', 'name': 'Enw', 'build_network': 'Creu_Rhwydwaith', 'font_info': 'ffont_gwybodaeth', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
