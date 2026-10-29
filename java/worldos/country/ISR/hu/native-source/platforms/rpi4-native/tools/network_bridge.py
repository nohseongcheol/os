#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/híd_3de4fe3a.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('híd_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('híd_3de4fe3a')
    leképezés_ÉRTÉK = {'response': 'válasz_1262b476', 'parts': 'útvonal_komponens', 's': 'sztring_adat', 'i': '순번', 'close': 'Bezárás', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'bejegyzés_ÉRTÉK', 'flags': 'konfiguráció_BITS', 'ftp_port': 'fájlátvitel_portszám', 'args': 'argumentum_TÖMB', 'server': 'kiszolgáló_ÉRTÉK', 'data': 'adat', 'ethernet_input': 'Ethernet_bevitel', 'trace_packet': 'nyom_csomag', 'GATEWAY': 'átjáró_hardver_CÍM', 'rule': 'lénia_ÉRTÉK', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'gazda', 'ack': '확인번호', 'serial_port': 'COM_port_szám', 'readers': '읽기대상들', 'guest': 'vendég', 'destination': 'cél_adat_CÍM', 'ethernet_port': 'Ethernet_port', 'b': 'MPERC_ÉRTÉK', 'MAC': 'valódi_cím', 'arp': 'CÍM_felbontás_csomag', 'writable': '쓸수있음', 'direction': '방향', 'seq': 'rendel_szám', 'frame': 'végrehajtás_doboz', 'loop': 'Ciklus_ÉRTÉK', 'port': 'portszám', 'offset': 'Ofszet_ÉRTÉK', 'readable': '읽을수있음', 'c': 'kódpont', 'p': 'adat_pozíció', 'writers': '쓰기대상들', 'IP': 'internetcím_ÉRTÉK', 'e': '보조항목', 'n': 'cikk_DARAB', 'packet': 'csomag_adat', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'híd_3de4fe3a', 'window': 'Ablak', 'capture': 'kioszt'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
