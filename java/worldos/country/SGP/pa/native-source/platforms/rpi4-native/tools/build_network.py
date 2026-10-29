#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਬਿਲਡ_ਨੈਟਵਰਕ.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਬਿਲਡ_ਨੈਟਵਰਕ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਬਿਲਡ_ਨੈਟਵਰਕ')
    대응 = {'obj': 'ਮੰਜਿਲ_ਪਤਾ_ffac9b48', 'objects': 'ਮੰਜਿਲ_ਫ਼ਾਈਲਾਂ', 'library': 'ਪੁਸਤਕਾਲਾ', 'output': '출력결과', 'port': '접속번호', 'root': 'ਰੂਟ_ਪਤਾ', 'files': 'ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ', 'source': '원본자료', 'run': 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', 'flags': '설정비트', 'path': 'ਮਾਰਗ', 'build_network': 'ਬਣਾਓ_ਨੈਟਵਰਕ', 'cc': '시언어번역기', 'ar': 'ਸੰਗ੍ਰਹਿ_ਸਾਧਨ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
