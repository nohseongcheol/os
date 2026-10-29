#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/BLD_C_compilatore.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_C_compilatore', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('BLD_C_compilatore')
    mapping_VALORE = {'out': 'KR_dati', 'builtins': '내장연산', 'header': 'Intestazione_VALORE', 'sdk': 'kit_di_sviluppo', 'build_ccompiler': 'Crea_C_compilatore', 'i': '순번', 'elf': 'eseguibile', 'run': 'Esegui_comando', 'flags': 'configurazione_BITS', 'path': 'percorso', 'p': 'dati_funzione', 'cc': 'C_compilatore', 'obj': 'file_di_destinazione', 'flag': 'Impostazioni_VALORE', 'ld': 'linker_strumento', 'objects': 'meta_File', 'repo': 'archivio_percorso', 'v': '임시값', 'upstream': 'upstream', 'root': 'radice_e_mail', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nome', 'includes': '포함인수'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
