#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ਸਮੱਗਰੀ', 'e': '보조항목', 'connection': 'ਸਬੰਧ_e05f319b', 'f': 'ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ', 'peer': 'ਪਿਅਰ_ਕੀਮਤ', 'self': '자신', 'udp': '전문제어', 't': 'ਟਰਮੀਨਲ_ਦਾਖਲਾ', 'tcp': 'ਸਬੰਧ_ਨਿਯੰਤਰਣ', 'EchoFixture': '되돌림시험서버', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
