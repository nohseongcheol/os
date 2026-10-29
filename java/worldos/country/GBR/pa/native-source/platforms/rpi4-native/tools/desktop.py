#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ਗਲਤੀ', 'exact': '정확한값', 'network': 'ਨੈਟਵਰਕ', 'closed': '닫힘', 'length': 'ਲੰਬਾਈ_ਕੀਮਤ', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'ਸਰਵਰ_ਕੀਮਤ', 'resources': 'ਸੋਮੇ', 'data': 'ਸਮੱਗਰੀ', 'shift': 'SHIFT_ਕੀ', 'send': 'ਈਮੇਲ', 'run_desktop': 'ਚਲਾਉ_ਡੈਸਕਟੌਪ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ਹੋਸਟ', 'text': 'ਟੈਕਸਟ', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'ਬਰਿਜ', 'kind': 'ਸ਼੍ਰੇਣੀ_ਕੀਮਤ', 'tail': '끝부분', 'size': 'ਆਕਾਰ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'ਗਾਹਕ', 'char': 'ਵਰਣ_ਸਮੱਗਰੀ', 'work': '작업경로', 'Keyboard': 'ਕੀਬੋਰਡ', 'x': 'x_ਕੌਔਰਡੀਨੇਟ', 'down': '누르는중', 'net': 'ਨੈਟਵਰਕ_ਬਰਿਜ_ਦਾਖਲਾ', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'ਪਰੋਸੈੱਸ', 'Desktop': 'ਕਨੈਕਟ_ਕਰੋ_ਡੈਸਕਟੌਪ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ਸਵਿੱਚ_ਮੋਡ', 'command': 'ਕਮਾਂਡ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_ਕੀ', 'path': 'ਮਾਰਗ', 'cp': 'ਵਰਣ_ਸੁਰੂ_ਤੋਂ_ਗਿਣਨਾ', 'terminate': '종료시키기', 'security': 'ਸੁਰੱਖਿਆ', 'vnc_port': '원격화면접속번호', 'body': 'ਮੁੱਖ_ਪਾਠ', 'index': 'ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ', 'exited': '종료됨', 'keysym': 'ਕੀ_ਪ੍ਰਤੀਕ', 'output': '출력결과', 'keyboard': 'ਕੀਬੋਰਡ_ਦਾਖਲਾ', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'ਪਾਠਕ', 'NetworkBridge': 'ਨੈਟਵਰਕ_ਬਰਿਜ', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
