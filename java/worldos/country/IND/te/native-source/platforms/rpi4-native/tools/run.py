#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('అమలు_చేయి_ఆదేశం', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('అమలు_చేయి_ఆదేశం')
    대응 = {'supported': '지원목록', 'parser': 'పార్సర్', 'qemu': '모의기계', 'run_desktop': 'అమలు_చెయ్_డెస్క్_టాప్', 'main': 'నడుపుము', 'host': 'హోస్ట్', 'status': 'స్థితి_మూల్యం', 'NetworkBridge': 'నెట్_వర్క్_బ్రిడ్జ్', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'bridge': 'బ్రిడ్జ్', 'loader': '적재기', 'base': 'నేపథ్యం_మూల్యం', 'options': 'ఐచ్ఛికాలు', 'binary': 'బైనరీ', 'args': 'కారకం_శ్రేణి', 'command': 'ఆదేశము'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
