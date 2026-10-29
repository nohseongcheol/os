#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/BLD_rete.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_rete', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('BLD_rete')
    mapping_VALORE = {'obj': 'file_di_destinazione', 'objects': 'meta_File', 'library': 'Catalogo', 'output': 'output', 'port': 'numero_di_porta', 'root': 'radice_e_mail', 'files': 'elenco_file', 'source': '원본자료', 'run': 'Esegui_comando', 'flags': 'configurazione_BITS', 'path': 'percorso', 'build_network': 'Crea_rete', 'cc': 'C_compilatore', 'ar': 'Archivio_strumento'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
