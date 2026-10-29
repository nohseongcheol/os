#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/예제되돌림서버.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('예제되돌림서버')
    mapping_VALORE = {'data': 'dati', 'sock': 'socket_VALORE', 'tcp_port': 'porta_TCP', 'chunk': 'blocco_VALORE_652d4b53', 'received': '수신됨', 'self': '자신', 'UDP': 'datagramma_handle_richiesta', 'thread': 'esecutoreAsincrono', 'echo': 'eco_schermo_server_voce', 'TCP': 'handle_connessione_richiesta', 'EchoServers': 'eco_schermo_Server', 'parser': 'parser', 'server': 'server_VALORE', 'udp_port': 'UDP_porta', 'args': 'argomento_array'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
