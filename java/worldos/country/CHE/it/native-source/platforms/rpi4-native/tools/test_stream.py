#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/test_Stream.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('test_Stream', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('test_Stream')
    mapping_VALORE = {'out': 'KR_dati', 'main': 'avvia', 'ROOT': 'azione_radice', 'p': 'dati_funzione', 'text': 'testo', 'report': 'convalida_Report'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
