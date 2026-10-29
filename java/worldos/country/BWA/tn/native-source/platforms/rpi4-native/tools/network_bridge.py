#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/Neteweke_leborogo.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('Neteweke_leborogo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Neteweke_leborogo')
    대응 = {'response': '응답자료', 'parts': 'tsela_karolwana', 's': 'dikwalwa_tshedimosetso', 'i': '순번', 'close': 'tswala', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'tsenyo_Boleng', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'Thulaganyo_setlhopha', 'server': 'sefara_Boleng', 'data': 'tshedimosetso', 'ethernet_input': '이더넷입력', 'trace_packet': 'palo_tlhakanyo_sephuthelwana', 'GATEWAY': '관문기계주소', 'rule': 'molawana_Boleng', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'pinagare', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'moeng', 'destination': 'bogorogelo_tshedimosetso_aterese', 'ethernet_port': 'Ithanete_gorogisetsa', 'b': '둘째값', 'MAC': 'motšhine_aterese', 'arp': 'aterese_resolušene_sephuthelwana', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Sediko_Boleng', 'port': '접속번호', 'offset': 'Baya_ka_Tekatekanyo_Boleng', 'readable': '읽을수있음', 'c': 'khoutuletshwao', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'aterese_ya_Inthanete_Boleng', 'e': '보조항목', 'n': '개수', 'packet': 'sephuthelwana_tshedimosetso', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Neteweke_leborogo', 'window': 'fensetere', 'capture': 'tshwara'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
