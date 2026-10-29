#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/되돌림시험서버.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('되돌림시험서버')
    toewijzing_WAARDE = {'data': 'gegevens', 'e': '보조항목', 'connection': 'verbinding_e05f319b', 'f': 'Bestand_invoer', 'peer': 'peer_WAARDE', 'self': '자신', 'udp': 'datagram_controle', 't': 'Terminal_invoer', 'tcp': 'verbinding_controle', 'EchoFixture': '되돌림시험서버', 'args': 'argument_MATRIX', 'chunk': '조각'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
