#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/SDK_compilare.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('SDK_compilare', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('SDK_compilare')
    mapping_VALORE = {'compiler': 'compilatore_strumento', 'obj': 'file_di_destinazione', 'sdk': 'kit_di_sviluppo', 'output': 'output', 'main': 'avvia', 'elf': 'eseguibile', 'is_c': 'reparto_IT_C_Lingua', 'parser': 'parser', 'language': 'Lingua', 'work': '작업경로', 'args': 'argomento_array'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
