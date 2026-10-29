#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ')
    대응 = {'data': 'ਸਮੱਗਰੀ', 'i': '순번', 'name': 'ਨਾਂ', 'c': 'ਵਰਣ_ਕੋਡ', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
