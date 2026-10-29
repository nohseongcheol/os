#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/sare_zubi.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('sare_zubi', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('sare_zubi')
    대응 = {'response': 'erantzun_1262b476', 'parts': 'bide_izen_osagai', 's': 'kate_datuak', 'i': '순번', 'close': 'Itxi', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'sarrera_balio', 'flags': 'konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna', 'ftp_port': 'fitxategi_transferitu_ataka_zenbaki', 'args': 'arg_matrize', 'server': 'zerbitzari_balio', 'data': 'datuak', 'ethernet_input': '이더넷입력', 'trace_packet': 'balio_diagonalen_batura_pakete', 'GATEWAY': '관문기계주소', 'rule': 'arau_balio', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'Ostalari', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'gonbidatu', 'destination': 'helburu_datuak_helbide', 'ethernet_port': 'Ethernet_ataka', 'b': 'SEGUNDOA_balio', 'MAC': 'gailu_helbide', 'arp': 'helbide_bereizmen_pakete', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Zikloa_balio', 'port': 'ataka_zenbaki', 'offset': 'Geruzak_balio', 'readable': '읽을수있음', 'c': 'karaktere_kode', 'p': 'datuak_kargu', 'writers': '쓰기대상들', 'IP': 'Internet_helbide_balio', 'e': '보조항목', 'n': 'elementu_ZENBATU', 'packet': 'pakete_datuak', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'sare_zubi', 'window': 'Leihoa', 'capture': 'atera_ba7b8054'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
