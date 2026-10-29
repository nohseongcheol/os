#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/అప్_లోడ్_ఫైల్_లు.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('అప్_లోడ్_ఫైల్_లు', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('అప్_లోడ్_ఫైల్_లు')
    대응 = {'data': 'డేటా', 'i': '순번', 'name': 'పేరు', 'c': 'అక్షర_కోడ్', 'p': 'డేటా_స్థాయి', 'args': 'కారకం_శ్రేణి'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
