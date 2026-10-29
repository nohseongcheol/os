#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/BLD_PYTHON.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_PYTHON', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('BLD_PYTHON')
    mapping_VALORE = {'ld': 'linker_strumento', 'archive': 'Archivio', 'SHA256': 'convalida_hash', 'build_python': 'Crea_PYTHON', 'root': 'radice_e_mail', 'source': '원본자료', 'name': 'Nome', 'path': 'percorso', 'VERSION': 'edizione_VALORE', 'cc': 'C_compilatore', 'tar': 'tar_aggregare', 'newlib': '뉴리브포함경로', 'member': 'membro'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
