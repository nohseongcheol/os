#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/셸시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_ਕੌਔਰਡੀਨੇਟ', 'msg': 'ਨੈਟਵਰਕ_ਸੁਨੇਹਾ', 'i': '순번', 'reply': 'ਜਵਾਬ_ਦਿਓ', 'call': '호출', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ', 'chunk': '조각', 'data': 'ਸਮੱਗਰੀ', 'proc': 'ਪਰੋਸੈੱਸ', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ਈਮੇਲ', 'file': 'ਫਾਇਲ', 'main': 'ਚਲਾਓ_2', 'found': 'ਖੋਜ_ਮਾਪ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'text': 'ਟੈਕਸਟ', 'marker': '확인표시', 'command': 'ਕਮਾਂਡ', 'expected': '예상결과', 'pixel': 'ਬਿੰਦੂ', 'shell': 'ਸ਼ੈਲ', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ਅੰਤ_ਔਫਸੈਟ', 'image': 'ਤਸਵੀਰ', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'ਮਾਪ', 'client': 'ਗਾਹਕ', 'line': 'ਲਾਈਨ', 'stream': 'ਸਟ੍ਰੀਮ_ਕੀਮਤ', 'name': 'ਨਾਂ', 'value': 'ਕੀਮਤ', 'receive': '수신하기', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
