#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ')
    대응 = {'timeout': '시간제한', 's': 'ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ', 'i': '순번', 'match': '일치', 'files': 'ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ', 'program': 'ਐਪਲੀਕੇਸ਼', 'executable': '실행가능파일', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ', 'chunk': '조각', 'data': 'ਸਮੱਗਰੀ', 'proc': 'ਪਰੋਸੈੱਸ', 'send': 'ਈਮੇਲ', 'main': 'ਚਲਾਓ_2', 'marker': '확인표시', 'command': 'ਕਮਾਂਡ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'parser': '인수해석기', 'options': 'ਚੋਣਾਂ', 'kind': 'ਸ਼੍ਰੇਣੀ_ਕੀਮਤ', 'selector': 'ਚੋਣਕਰਤਾ', 'upload_data': 'ਅਪਲੋਡ_ਕਰੋ_ਸਮੱਗਰੀ', 'end': 'ਅੰਤ_ਔਫਸੈਟ', 'n': '개수', 'd': 'ਮੰਜਿਲ_ਸਮੱਗਰੀ', 'key': '누름값', 'output': '출력결과', 'line': 'ਲਾਈਨ', 'name': 'ਨਾਂ', 'upload_name': 'ਅਪਲੋਡ_ਕਰੋ_ਨਾਮ', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
