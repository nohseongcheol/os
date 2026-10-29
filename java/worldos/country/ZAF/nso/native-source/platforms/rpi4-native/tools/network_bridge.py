#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/Netweke_kgokaganyo.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('Netweke_kgokaganyo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Netweke_kgokaganyo')
    대응 = {'response': '응답자료', 'parts': 'tsela_karolo', 's': 'molokoloko_data', 'i': '순번', 'close': 'Tswalela', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'go_tsenya_tshedimošo_boleng', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'akumente_arei', 'server': 'seba_boleng', 'data': 'data', 'ethernet_input': '이더넷입력', 'trace_packet': 'latišiša_sephuthelwana', 'GATEWAY': '관문기계주소', 'rule': 'filthara_boleng', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'go_nea_ditirelo', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'moeng', 'destination': 'boyo_data_atrese', 'ethernet_port': 'Ethenete_phote', 'b': '둘째값', 'MAC': 'atrese_ya_kgonthe', 'arp': 'atrese_sephetho_sephuthelwana', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'sediko_boleng', 'port': '접속번호', 'offset': 'E_Šetšego_boleng', 'readable': '읽을수있음', 'c': 'khouto_ya_tlhaka', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'atrese_ya_Inthanete_boleng', 'e': '보조항목', 'n': '개수', 'packet': 'sephuthelwana_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Netweke_kgokaganyo', 'window': 'lefastere', 'capture': 'tšea'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
