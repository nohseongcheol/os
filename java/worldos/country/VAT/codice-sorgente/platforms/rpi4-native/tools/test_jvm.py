#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/test_JVM.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('test_JVM', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('test_JVM')
    mapping_VALORE = {'message': 'informativa_SMS', 's': 'stringa_dati', 'actual': 'effettivo_KR', 'match': '일치', 'payload': 'payload_dati', 'cases': 'test_case', 'fixture': 'test_dati', 'main': 'avvia', 'ROOT': 'azione_radice', 'text': 'testo', 'valid': 'valido', 'includes': '포함인수', 'include': 'includere', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Completate_importo', 'classes': 'Corso_percorso', 'output': 'output', 'result': 'risultato', 'cmd': '명령인수', 'name': 'Nome', 'jar': '자바꾸러미', 'report': 'convalida_Report', 'tests': 'elenco_dei_test'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
