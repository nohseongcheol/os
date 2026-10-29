#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'Daten', 'e': '보조항목', 'connection': 'Verbindung_e05f319b', 'f': 'Fichier_Agab', 'peer': 'Peer_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_Agab', 'tcp': 'Verbindung_Kontroll', 'EchoFixture': '되돌림시험서버', 'args': 'Argument_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
