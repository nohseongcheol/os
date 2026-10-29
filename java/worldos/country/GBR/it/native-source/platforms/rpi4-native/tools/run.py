#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/Esegui_comando.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('Esegui_comando', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('Esegui_comando')
    mapping_VALORE = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'eseguire_PC', 'main': 'avvia', 'host': 'host', 'status': 'Stato_VALORE', 'NetworkBridge': 'bridge_3de4fe3a', 'ROOT': 'azione_radice', 'bridge': 'bridge', 'loader': 'caricatore', 'base': 'sfondo_VALORE', 'options': 'Opzioni', 'binary': 'base_2', 'args': 'argomento_array', 'command': 'comando'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
