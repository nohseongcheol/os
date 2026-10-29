#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/실행파일시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'ਮਾਪ_ਸਮੱਗਰੀ', 'expected': '예상결과', 'phoff': 'ਐਪਲੀਕੇਸ਼_ਸਿਰਲੇਖ_ਔਫਸੈਟ', 'offset': 'ਔਫਸੈਟ_ਕੀਮਤ', 'invalid': 'ਅਯੋਗ_ਸਮੱਗਰੀ', 'path': 'ਮਾਰਗ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ਮਾਪ', 'format_': 'ਸਰੂਪ_b87fd068', 'main': 'ਚਲਾਓ_2', 'content': 'ਤਤਕਰਾ_ਕੀਮਤ', 'source': '원본자료', 'name': 'ਨਾਂ', 'reference': '비교기준', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'value': 'ਕੀਮਤ', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
