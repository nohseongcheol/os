#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/예제빌드.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'ਮਾਪ_ਸਮੱਗਰੀ', 'build_examples': '예제만들기', 'files': 'ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ', 'java': '자바실행', 'run': 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', 'path': 'ਮਾਰਗ', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'readme': 'ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ', 'classes': 'ਸ੍ਰੇਣੀ_ਰਸਤਾ', 'repo': '저장소경로', 'root': 'ਰੂਟ_ਪਤਾ', 'content': 'ਤਤਕਰਾ_ਕੀਮਤ', 'source': '원본자료', 'name': 'ਨਾਂ', 'target': 'ਟੀਚਾ', 'manifest': '꾸러미명세', 'language': 'ਭਾਸ਼ਾ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
