#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/llunio_Rhwydwaith.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('llunio_Rhwydwaith', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('llunio_Rhwydwaith')
    대응 = {'obj': 'ffeil_derbyn', 'objects': 'cyrchfan_Ffeil', 'library': 'llyfrgell', 'output': '출력결과', 'port': 'rhif_porth', 'root': 'gwraidd_ADDRESS', 'files': 'ffeil_Rhestr', 'source': '원본자료', 'run': 'Gweithredu_gorchymyn', 'flags': '설정비트', 'path': 'LLWYBR', 'build_network': 'Creu_Rhwydwaith', 'cc': '시언어번역기', 'ar': 'Archif_offeryn'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
