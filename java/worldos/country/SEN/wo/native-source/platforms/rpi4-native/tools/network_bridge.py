#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/mbaal_poŋ.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('mbaal_poŋ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('mbaal_poŋ')
    대응 = {'response': '응답자료', 'parts': 'Yoonu_jëmale_bu_ci_bokk', 's': 'araf_yu_bennoo_mbir', 'i': '순번', 'close': 'Tej', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'dugal_xabaar_xëyma', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'Tegtal_TABLO', 'server': 'dëggu_xëyma', 'data': 'mbir', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': 'bunt_jumtukaay_dëkkuwaay', 'rule': 'sart_xëyma', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'dalal', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'gan', 'destination': 'jëmmukaay_mbir_dëkkuwaay', 'ethernet_port': 'Ethernet_jël', 'b': '둘째값', 'MAC': 'masin_dëkkuwaay', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Wërngal_xëyma', 'port': '접속번호', 'offset': 'Randal_xëyma', 'readable': '읽을수있음', 'c': 'kotu_araf', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'dëkkuwaayu_Internet_xëyma', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'mbaal_poŋ', 'window': 'palanteer', 'capture': 'jël'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
