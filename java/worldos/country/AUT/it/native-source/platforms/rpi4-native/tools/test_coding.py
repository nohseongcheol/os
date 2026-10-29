#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/코딩시험.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('코딩시험')
    mapping_VALORE = {'out': 'KR_dati', 'expected': '예상결과', 'sdk': 'kit_di_sviluppo', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'avvia', 'elf': 'eseguibile', 'run': 'Esegui_comando', 'name': 'Nome', 'path': 'percorso', 'p': 'dati_funzione', 'ROOT': 'azione_radice', 'report': 'convalida_Report', 'args': 'argomento_array'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
