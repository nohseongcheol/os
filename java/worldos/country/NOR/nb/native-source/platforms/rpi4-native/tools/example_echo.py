#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/예제되돌림서버.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('예제되돌림서버')
    tildeling_VERDI = {'data': 'data', 'sock': 'socket_VERDI', 'tcp_port': 'TCP_port', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': 'datagram_håndtak_forespørsel', 'thread': 'arbeider', 'echo': 'oppdatere_skjerm_server_oppføring', 'TCP': 'håndtak_kontakt_forespørsel', 'EchoServers': 'oppdatere_skjerm_Servere', 'parser': 'parser', 'server': 'server_VERDI', 'udp_port': 'UDP_port', 'args': 'argument_MATRISE'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
