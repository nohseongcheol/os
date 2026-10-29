#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/예제되돌림서버.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('예제되돌림서버')
    leképezés_ÉRTÉK = {'data': 'adat', 'sock': 'szoftvercsatorna_ÉRTÉK', 'tcp_port': 'TCP_port', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': 'datagram_leíró_kérés', 'thread': 'dolgozó', 'echo': 'visszhang_kiszolgáló_bejegyzés', 'TCP': 'leíró_ismerős_kérés', 'EchoServers': 'visszhang_Kiszolgálók', 'parser': 'elemző', 'server': 'kiszolgáló_ÉRTÉK', 'udp_port': 'UDP_port', 'args': 'argumentum_TÖMB'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
