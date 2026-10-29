#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/바탕화면시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_ਕੌਔਰਡੀਨੇਟ', 'typing': '글자입력', 'message': '알림문', 'start': 'ਚਲਾਓ_2', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'ਪ੍ਰਤੀਕ', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'ਪਰੋਸੈੱਸ', 'data': 'ਸਮੱਗਰੀ', 'main': 'ਚਲਾਓ_2', 'w': '너비값', 'init': '초기값', 'block': 'ਸਮੱਗਰੀ_ਬਲੌਕ_ਕਰੋ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'text': 'ਟੈਕਸਟ', 'marker': '확인표시', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ', 'until': '까지', 'clipboard': 'ਕਲਿਪਬੋਰਡ_ਕੀਮਤ', 'dst': 'ਮੰਜਿਲ_ਪਤਾ', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'ਔਫਸੈਟ_ਕੀਮਤ', 'h': '높이값', 'src': '원본주소', 'event': 'ਇਵੈਂਟ', 'encoding': 'ਵਰਣ_ਸੈਟ', 'size': 'ਆਕਾਰ', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'ਪ੍ਰਤੀਕ_ਕੀਮਤ', 'client': 'ਗਾਹਕ', 'char': 'ਵਰਣ_ਸਮੱਗਰੀ', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
