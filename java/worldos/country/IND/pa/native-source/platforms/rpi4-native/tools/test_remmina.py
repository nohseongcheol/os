#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/원격한글시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ਚਲਾਓ_2', 'profile': 'ਪ੍ਰੋਫਾਈਲ', 'focused': 'ਫੋਕਸ_f7e69dab', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'ਸਰਵਰ_ਕੀਮਤ', 'log': 'ਲੌਗ_ਕਤਾਰ', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ', 'deadline': '마감시각', 'data': 'ਸਮੱਗਰੀ', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ਚਲਾਓ_2', 'ready': '준비완료', 'found': 'ਖੋਜ_ਮਾਪ', 'guest': 'ਗੈਸਟ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'marker': '확인표시', 'text': 'ਟੈਕਸਟ', 'out': 'ਮਾਪ_ਸਮੱਗਰੀ', 'env': '환경', 'f': 'ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ', 'port': '접속번호', 'offset': 'ਔਫਸੈਟ_ਕੀਮਤ', 'version': '판번호', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'selector': 'ਚੋਣਕਰਤਾ', 'xvfb': 'ਵਰਚੁਅਲ_ਪ੍ਰਦਰਸ਼ਨ', 'display': 'ਪ੍ਰਦਰਸ਼ਨ', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ਨਾਂ', 'window': 'ਵਿੰਡੋ', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
