#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/예제되돌림서버.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('예제되돌림서버')
    tilknytning_VÆRDI = {'data': 'data', 'sock': 'socket_VÆRDI', 'tcp_port': 'TCP_port', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': 'datagram_handle_anmodning', 'thread': 'arbejder', 'echo': 'ekko_server_post', 'TCP': 'handle_forbindelse_anmodning', 'EchoServers': 'ekko_Servere', 'parser': 'parser', 'server': 'server_VÆRDI', 'udp_port': 'UDP_port', 'args': 'argument_MATRIX'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
