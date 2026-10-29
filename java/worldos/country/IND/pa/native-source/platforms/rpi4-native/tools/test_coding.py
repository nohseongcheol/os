#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/코딩시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': 'ਮਾਪ_ਸਮੱਗਰੀ', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'ਚਲਾਓ_2', 'elf': '실행파일', 'run': 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', 'name': 'ਨਾਂ', 'path': 'ਮਾਰਗ', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
