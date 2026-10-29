#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਬਿਲਡ_ਟਰਮੀਨਲ_ਫੌਂਟ.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਬਿਲਡ_ਟਰਮੀਨਲ_ਫੌਂਟ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਬਿਲਡ_ਟਰਮੀਨਲ_ਫੌਂਟ')
    대응 = {'data': 'ਸਮੱਗਰੀ', 'img': 'ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ', 'bits': '비트들', 'x': 'x_ਕੌਔਰਡੀਨੇਟ', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ਰਸਤਾ_ਸੂਚੀ', 'y': '세로좌표', 'main': 'ਚਲਾਓ_2', 'src': '원본주소', 'fonts': 'ਫੌਂਟ_ਸੂਚੀ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'cp': 'ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ', 'target': 'ਟੀਚਾ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
