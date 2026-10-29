#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਨੈਟਵਰਕ_ਬਰਿਜ.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਨੈਟਵਰਕ_ਬਰਿਜ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਨੈਟਵਰਕ_ਬਰਿਜ')
    대응 = {'response': '응답자료', 'parts': 'ਰਸਤਾ_ਅੰਗ', 's': 'ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ', 'i': '순번', 'close': 'ਬੰਦ_ਕਰੋ', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ਦਾਖਲਾ_ਕੀਮਤ', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ', 'server': 'ਸਰਵਰ_ਕੀਮਤ', 'data': 'ਸਮੱਗਰੀ', 'ethernet_input': '이더넷입력', 'trace_packet': 'ਟਰੇਸ_ਪੈਕੇਟ', 'GATEWAY': '관문기계주소', 'rule': 'ਨਿਯਮ_ਕੀਮਤ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'ਹੋਸਟ', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'ਗੈਸਟ', 'destination': 'ਮੰਜਿਲ_ਸਮੱਗਰੀ_ਪਤਾ', 'ethernet_port': 'ਈਥਰਨੈਟ_ਪੋਰਟ', 'b': '둘째값', 'MAC': 'ਮਸ਼ੀਨ_ਪਤਾ', 'arp': 'ਪਤਾ_ਰੂਪਾਂਤਰ_ਪੈਕੇਟ', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'ਸਾਇਕਲ_ਕੀਮਤ', 'port': '접속번호', 'offset': 'ਔਫਸੈਟ_ਕੀਮਤ', 'readable': '읽을수있음', 'c': 'ਵਰਣ_ਕੋਡ', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'writers': '쓰기대상들', 'IP': 'ਇੰਟਰਨੈਟ_ਪਤਾ_ਕੀਮਤ', 'e': '보조항목', 'n': '개수', 'packet': 'ਪੈਕੇਟ_ਸਮੱਗਰੀ', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'ਨੈਟਵਰਕ_ਬਰਿਜ', 'window': 'ਵਿੰਡੋ', 'capture': 'ਪਕੜਨਾ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
