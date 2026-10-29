#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/예제시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'ਸਮੱਗਰੀ', 'graphics_command': 'ਗਰਾਫਿਕਸ_ਆਦੇਸ਼', 'main': 'ਚਲਾਓ_2', 'row': 'ਕਤਾਰ_ਸਥਿਤੀ_ਬਦਲੋ', 'init': '초기값', 'target': 'ਟੀਚਾ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'text': 'ਟੈਕਸਟ', 'binary': 'ਜੋੜੇਦਾਰ', 'out': 'ਮਾਪ_ਸਮੱਗਰੀ', 'entry': 'ਦਾਖਲਾ_ਪੌਇੰਟ', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'ਸੁਰੂ_ਚਿੱਤਰ_ਬਨਾਉਣਾ', 'col': 'ਕੋਲਮ_ਸਥਿਤੀ_ਬਦਲੋ', 'begin': 'ਸੁਰੂ_ਔਫਸੈਟ', 'kind': 'ਸ਼੍ਰੇਣੀ_ਕੀਮਤ', 'selector': 'ਚੋਣਕਰਤਾ', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'ਗਾਹਕ', 'line': 'ਲਾਈਨ', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ', 'language': 'ਭਾਸ਼ਾ', 'x': 'x_ਕੌਔਰਡੀਨੇਟ', 'start': 'ਚਲਾਓ_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ਈਮੇਲ_ਸੂਚੀ', 'payload': 'ਪੇਲੋਡ_ਸਮੱਗਰੀ', 'proc': 'ਪਰੋਸੈੱਸ', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ਨਾਮ_ਤਾਲਿਕਾ', 'content': 'ਤਤਕਰਾ_ਕੀਮਤ', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ', 'shell': 'ਸ਼ੈਲ', 'color': '색상', 'transcript': '대화기록', 'offset': 'ਔਫਸੈਟ_ਕੀਮਤ', 'h': '높이값', 'run': 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', 'c': 'ਵਰਣ_ਕੋਡ', 'path': 'ਮਾਰਗ', 'encoding': 'ਵਰਣ_ਸੈਟ', 'end': 'ਅੰਤ_ਔਫਸੈਟ', 'ftp': 'ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ', 'pixels': '화소들', 'symbol': 'ਪ੍ਰਤੀਕ_ਕੀਮਤ', 'source': '원본자료', 'name': 'ਨਾਂ', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
