#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'ਸਿਰਲੇਖ_ਕੀਮਤ', 'sources': '원문목록', 'i': '순번', 'info': 'ਸਿਸਟਮ_ਜਾਣਕਾਰੀ', 'payload': 'ਪੇਲੋਡ_ਸਮੱਗਰੀ', 'src': '원본주소', 'run': 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'ਸ੍ਰੇਣੀ_ਰਸਤਾ', 'dist': '배포경로', 'archive': 'ਸੰਗ੍ਰਹਿ', 'output': '출력결과', 'root': 'ਰੂਟ_ਪਤਾ', 'name': 'ਨਾਂ', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
