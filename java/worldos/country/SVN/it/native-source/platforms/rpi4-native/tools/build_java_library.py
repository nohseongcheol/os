#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/자바라이브러리빌드.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('자바라이브러리빌드')
    mapping_VALORE = {'header': 'Intestazione_VALORE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'payload_dati', 'src': '원본주소', 'run': 'Esegui_comando', 'build_java_library': '자바라이브러리만들기', 'relative': 'percorso_relativo', 'classes': 'Corso_percorso', 'dist': 'distribuzione_percorso', 'archive': 'Archivio', 'output': 'output', 'root': 'radice_e_mail', 'name': 'Nome', 'jar': '자바꾸러미', 'b': 'SECONDO_VALORE', 'entries': '항목들'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
