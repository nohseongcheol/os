#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/파일전송시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ਪੇਲੋਡ_ਸਮੱਗਰੀ', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ਸਮੱਗਰੀ', 'proc': 'ਪਰੋਸੈੱਸ', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ਸੰਗ੍ਰਹਿ', 'main': 'ਚਲਾਓ_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ਸਥਾਈ_ਸਰੋਤ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'text': 'ਟੈਕਸਟ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ਕਮਾਂਡ', 'out': 'ਮਾਪ_ਸਮੱਗਰੀ', 'expected': '예상결과', 'server_source': 'ਸਰਵਰ_ਸਰੋਤ', 'shell': 'ਸ਼ੈਲ', 'upload': 'ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ਬਰਿਜ', 'selector': 'ਚੋਣਕਰਤਾ', 'end': 'ਅੰਤ_ਔਫਸੈਟ', 'e': '보조항목', 'ftp': 'ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ਪਿਅਰ_ਕੀਮਤ', 'result': 'ਮਾਪ', 'unchanged': '보존자료', 'line': 'ਲਾਈਨ', 'server_tcp_port': 'ਸਰਵਰ_ਸਟ੍ਰੀਮ_ਪੋਰਟ', 'source': '원본자료', 'NetworkBridge': 'ਨੈਟਵਰਕ_ਬਰਿਜ', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
