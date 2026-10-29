#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/eco_schermo_fixture.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('eco_schermo_fixture', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('eco_schermo_fixture')
    mapping_VALORE = {'data': 'dati', 'e': '보조항목', 'connection': 'connessione_e05f319b', 'f': 'File_voce', 'peer': 'peer_VALORE', 'self': '자신', 'udp': 'datagramma_controllo', 't': 'Terminale_voce', 'tcp': 'connessione_controllo', 'EchoFixture': 'eco_schermo_fixture', 'args': 'argomento_array', 'chunk': 'blocco_VALORE_652d4b53'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
