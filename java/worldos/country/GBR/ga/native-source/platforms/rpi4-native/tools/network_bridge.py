#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/Líonra_traschóiritheoir.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('Líonra_traschóiritheoir', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Líonra_traschóiritheoir')
    대응 = {'response': '응답자료', 'parts': 'cosán_comhpháirt', 's': 'teaghrán_sonraí', 'i': '순번', 'close': 'Dún', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'iontráil_VALUE', 'flags': '설정비트', 'ftp_port': 'comhad_traschur_uimhir_phoirt', 'args': 'argóint_ARRAY', 'server': 'freastalaí_VALUE', 'data': 'sonraí', 'ethernet_input': '이더넷입력', 'trace_packet': 'rian_paicéad', 'GATEWAY': '관문기계주소', 'rule': 'riail_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'óstach', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'aoi', 'destination': 'sprioc_sonraí_ADDRESS', 'ethernet_port': 'Ethernet_port', 'b': 'SECOND_VALUE', 'MAC': 'meaisín_ADDRESS', 'arp': 'ADDRESS_taifeach_paicéad', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Timthriall_VALUE', 'port': 'uimhir_phoirt', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'pointe_cóid', 'p': 'sonraí_suíomh', 'writers': '쓰기대상들', 'IP': 'seoladh_Idirlín_VALUE', 'e': '보조항목', 'n': 'mír_COUNT', 'packet': 'paicéad_sonraí', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Líonra_traschóiritheoir', 'window': 'fuinneog', 'capture': 'taifead'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
