#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/iNethiwekhi_ibhuloho.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('iNethiwekhi_ibhuloho', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('iNethiwekhi_ibhuloho')
    대응 = {'response': '응답자료', 'parts': 'umzila_isixa', 's': 'uchunge_imininingwane', 'i': '순번', 'close': 'Vala', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'okufakwayo_inani', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'i_agumenti_AMALUNGU_AFANAYO', 'server': 'Iseva_inani', 'data': 'imininingwane', 'ethernet_input': '이더넷입력', 'trace_packet': 'ithreyisi_iphakethe', 'GATEWAY': '관문기계주소', 'rule': 'ihluzo_inani', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'singatha', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'isivakashi', 'destination': 'isikhumulo_imininingwane_ikheli', 'ethernet_port': 'i_Ethernet_intuba', 'b': '둘째값', 'MAC': 'umshini_ikheli', 'arp': 'ikheli_ukucaca_iphakethe', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Umjikelezo_inani', 'port': '접속번호', 'offset': 'I_ofisethi_inani', 'readable': '읽을수있음', 'c': 'ikhodi_yohlamvu', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'ikheli_le_inthanethi_inani', 'e': '보조항목', 'n': '개수', 'packet': 'iphakethe_imininingwane', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'iNethiwekhi_ibhuloho', 'window': 'ifasitela', 'capture': 'thwebula'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
