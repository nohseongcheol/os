#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/lìonra_drochaid.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('lìonra_drochaid', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('lìonra_drochaid')
    대응 = {'response': '응답자료', 'parts': 'slighe_co_phàirt', 's': 'sreang_dàta', 'i': '순번', 'close': 'dùin', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'cur_a_steach_VALUE', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'argamaid_ARRAY', 'server': 'frithealaiche_VALUE', 'data': 'dàta', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'criathrag_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'òstair', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'aoigh', 'destination': 'ceann_uidhe_dàta_ADDRESS', 'ethernet_port': 'Ethernet_port', 'b': 'SECOND_VALUE', 'MAC': 'inneal_ADDRESS', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'cuairt_VALUE', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'còd_a_charactair', 'p': 'dàta_suidhich', 'writers': '쓰기대상들', 'IP': 'Seòladh_eadar_lìn_VALUE', 'e': '보조항목', 'n': 'nì_COUNT', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'lìonra_drochaid', 'window': 'uinneag', 'capture': 'glac'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
