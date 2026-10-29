#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/Şəbəkə_körpü.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('Şəbəkə_körpü', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Şəbəkə_körpü')
    대응 = {'response': 'video_münasibət', 'parts': 'yol_komponent', 's': 'sətir_verilənlər', 'i': '순번', 'close': 'Bağla', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'daxiletmə_VALUE', 'flags': 'konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti', 'ftp_port': '파일전송접속번호', 'args': 'arqument_ARRAY', 'server': 'server_VALUE', 'data': 'verilənlər', 'ethernet_input': '이더넷입력', 'trace_packet': 'iz_paket', 'GATEWAY': '관문기계주소', 'rule': 'qayda_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'host', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'qonaq', 'destination': 'təyinat_verilənlər_ünvan', 'ethernet_port': 'Ethernet_ə_qoşma_yuvası', 'b': 'SECOND_VALUE', 'MAC': 'maşın_ünvan', 'arp': 'ünvan_əksetmə_qabiliyyəti_paket', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Dövrə_VALUE', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'simvol_kodu', 'p': 'verilənlər_yerinə_qoymaq', 'writers': '쓰기대상들', 'IP': 'İnternet_ünvanı_VALUE', 'e': '보조항목', 'n': 'element_COUNT', 'packet': 'paket_verilənlər', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Şəbəkə_körpü', 'window': 'pəncərə', 'capture': 'çəkmək'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
