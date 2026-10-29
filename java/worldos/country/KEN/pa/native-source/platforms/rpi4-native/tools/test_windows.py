#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/창시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'x_ਕੌਔਰਡੀਨੇਟ', 's': 'ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ', 'xy': 'ਕੋਔਰਡੀਨੇਟ_ਪੇਅਰ', 'sel': 'ਚੋਣਕਰਤਾ_a916db4e', 'seconds': '초단위', 'log': 'ਲੌਗ_ਕਤਾਰ', 'at': '현재위치', 'send': 'ਈਮੇਲ', 'main': 'ਚਲਾਓ_2', 'req': '요청값', 'hot': 'ਸ਼ੌਰਟਕਟ_ਕੀਮਤ', 'pump': 'ਸੰਭਾਲਣਾ_ਇਵੈਂਟ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'marker': '확인표시', 'b': '둘째값', 'command': 'ਕਮਾਂਡ', 'shell': 'ਸ਼ੈਲ', 'f': 'ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ', 'color': '색상', 'click': 'ਕਲਿਕ_ਕਰੋ_ਬਟਨ', 'k': '셋째순번', 'c': 'ਵਰਣ_ਕੋਡ', 'r': '반환값', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'done': '완료량', 'end': 'ਅੰਤ_ਔਫਸੈਟ', 'command_mode': 'ਆਦੇਸ਼_ਮੋਡ', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'ਮਾਪ', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ', 'dest': 'ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
