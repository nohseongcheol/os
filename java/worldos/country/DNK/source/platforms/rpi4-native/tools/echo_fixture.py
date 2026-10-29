#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/되돌림시험서버.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('되돌림시험서버')
    tilknytning_VÆRDI = {'data': 'data', 'e': '보조항목', 'connection': 'forbindelse_e05f319b', 'f': 'fil_post', 'peer': 'peer_VÆRDI', 'self': '자신', 'udp': 'datagram_kontrol', 't': 'Terminal_post', 'tcp': 'forbindelse_kontrol', 'EchoFixture': '되돌림시험서버', 'args': 'argument_MATRIX', 'chunk': '조각'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
