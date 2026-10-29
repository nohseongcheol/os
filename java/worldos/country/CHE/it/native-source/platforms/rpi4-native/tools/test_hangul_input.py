#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/한글입력시험.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('한글입력시험')
    mapping_VALORE = {'expected': '예상결과', 'Keyboard': 'tastiera', 'press': '글쇠누르기', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_incollare_E_UNICODE', 'data': 'dati', 'key': '누름값', 'send': 'inviare', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'simbolo_VALORE', 'char': 'dati_di_tipo_carattere', 'type': 'TIPO_area'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
