#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ਚਲਾਉ_ਡੈਸਕਟੌਪ', 'main': 'ਚਲਾਓ_2', 'host': 'ਹੋਸਟ', 'status': 'ਸਥਿਤੀ_ਕੀਮਤ', 'NetworkBridge': 'ਨੈਟਵਰਕ_ਬਰਿਜ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'bridge': 'ਬਰਿਜ', 'loader': '적재기', 'base': 'ਪਿਛੋਕੜ_ਕੀਮਤ', 'options': 'ਚੋਣਾਂ', 'binary': 'ਜੋੜੇਦਾਰ', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ', 'command': 'ਕਮਾਂਡ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
