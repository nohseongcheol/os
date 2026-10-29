#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/esportare_SDK.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('esportare_SDK', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('esportare_SDK')
    mapping_VALORE = {'out': 'KR_dati', 'obj': 'file_di_destinazione', 'relative': 'percorso_relativo', 'compiler_archive': 'compilatore_Archivio', 'sdk': 'kit_di_sviluppo', 'dist': 'distribuzione_percorso', 'archive': 'Archivio', 'main': 'avvia', 'posix': '포직스경로', 'files': 'elenco_file', 'source': '원본자료', 'name': 'Nome', 'target': 'target', 'ROOT': 'azione_radice', 'destination': 'meta_dati_e_mail', 'manifest': 'aggregare_manifesto', 'work': '작업경로'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
