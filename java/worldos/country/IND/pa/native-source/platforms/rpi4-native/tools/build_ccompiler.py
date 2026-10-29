#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'ਮਾਪ_ਸਮੱਗਰੀ', 'builtins': '내장연산', 'header': 'ਸਿਰਲੇਖ_ਕੀਮਤ', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', 'flags': '설정비트', 'path': 'ਮਾਰਗ', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'cc': '시언어번역기', 'obj': 'ਮੰਜਿਲ_ਪਤਾ_ffac9b48', 'flag': 'ਸੈਟਿੰਗਾਂ_ਕੀਮਤ', 'ld': '연결편집기', 'objects': 'ਮੰਜਿਲ_ਫ਼ਾਈਲਾਂ', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'ਰੂਟ_ਪਤਾ', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ਨਾਂ', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
