#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/Upload_File.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('Upload_File', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('Upload_File')
    mapping_VALORE = {'data': 'dati', 'i': '순번', 'name': 'Nome', 'c': 'punto_di_codice', 'p': 'dati_funzione', 'args': 'argomento_array'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
