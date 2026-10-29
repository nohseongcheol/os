#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਬਣਾਓ_ਤਸਵੀਰ.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਬਣਾਓ_ਤਸਵੀਰ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਬਣਾਓ_ਤਸਵੀਰ')
    대응 = {'total': '총량', 'start': 'ਚਲਾਓ_2', 'firmware': '기초제어프로그램', 'files': 'ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ', 'archive_base': '압축기준', 'partition': 'ਵੰਡ_ਲਿਖਤ_ਪੱਤਰ', 'archive': 'ਸੰਗ੍ਰਹਿ', 'main': 'ਚਲਾਓ_2', 'block': 'ਸਮੱਗਰੀ_ਬਲੌਕ_ਕਰੋ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'boot': '부팅경로', 'stage': 'ਪੜਾਅ_ਕੀਮਤ', 'out': 'ਮਾਪ_ਸਮੱਗਰੀ', 'expected': '예상결과', 'f': 'ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ', 'src': '원본주소', 'path': 'ਮਾਰਗ', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'extracted': '추출자료', 'member': 'ਸਦੱਸ', 'mbr': '주부트기록', 'image': 'ਤਸਵੀਰ', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ਲਾਇਸੈਂਸ', 'source': '원본자료', 'name': 'ਨਾਂ', 'value': 'ਕੀਮਤ', 'manifest': '꾸러미명세', 'dest': 'ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
