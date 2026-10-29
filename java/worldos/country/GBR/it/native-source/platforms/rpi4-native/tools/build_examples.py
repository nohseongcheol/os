#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/예제빌드.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('예제빌드')
    mapping_VALORE = {'out': 'KR_dati', 'build_examples': '예제만들기', 'files': 'elenco_file', 'java': '자바실행', 'run': 'Esegui_comando', 'path': 'percorso', 'p': 'dati_funzione', 'readme': 'README', 'build_java_library': '자바라이브러리만들기', 'code': 'istruzione_SEQUENZA', 'index': 'CERCA_INDICE', 'classes': 'Corso_percorso', 'repo': 'archivio_percorso', 'root': 'radice_e_mail', 'content': 'Contenuto_VALORE', 'source': '원본자료', 'name': 'Nome', 'target': 'target', 'manifest': 'aggregare_manifesto', 'language': 'Lingua'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
