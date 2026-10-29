#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/개발꾸러미내보내기.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미내보내기')
    대응 = {'out': 'ਮਾਪ_ਸਮੱਗਰੀ', 'obj': 'ਮੰਜਿਲ_ਪਤਾ_ffac9b48', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'ਸੰਗ੍ਰਹਿ', 'main': 'ਚਲਾਓ_2', 'posix': '포직스경로', 'files': 'ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ', 'source': '원본자료', 'name': 'ਨਾਂ', 'target': 'ਟੀਚਾ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'destination': 'ਮੰਜਿਲ_ਸਮੱਗਰੀ_ਪਤਾ', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
