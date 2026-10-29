#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/تور_كۆۋرۈك.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('تور_كۆۋرۈك', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('تور_كۆۋرۈك')
    대응 = {'response': '응답자료', 'parts': 'يول_زاپچاس', 's': 'ھەرپ_تىزمىسى_مەلۇمات', 'i': '순번', 'close': 'ياپ', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'كىرگۈزۈش_قىممىتى', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'دەلىل_رەت', 'server': 'مۇلازىمىتېر_قىممىتى', 'data': 'مەلۇمات', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'سىزىق_قىممىتى', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'باقار', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'مېھمان', 'destination': 'نىشان_مەلۇمات_ئادرېس', 'ethernet_port': 'ئىسېرنېت_ئېغىز', 'b': '둘째값', 'MAC': 'ماشىنا_ئادرېس', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'دەۋرىي_قىممىتى', 'port': '접속번호', 'offset': 'ئاغما_قىممىتى', 'readable': '읽을수있음', 'c': 'ھەرپ_كودى', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'writers': '쓰기대상들', 'IP': 'ئىنتېرنېت_ئادرېسى_قىممىتى', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'تور_كۆۋرۈك', 'window': 'كۆزنەك', 'capture': 'تۇتۇش'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
