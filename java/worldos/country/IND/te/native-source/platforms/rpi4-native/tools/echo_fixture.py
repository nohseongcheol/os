#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/되돌림시험서버.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'డేటా', 'e': '보조항목', 'connection': 'కనెక్షన్_e05f319b', 'f': 'ఫైలు_ప్రవేశం', 'peer': 'పియర్_మూల్యం', 'self': '자신', 'udp': '전문제어', 't': 'టెర్మినల్_ప్రవేశం', 'tcp': 'కనెక్షన్_నియంత్రణ', 'EchoFixture': '되돌림시험서버', 'args': 'కారకం_శ్రేణి', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
