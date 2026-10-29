#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/한글입력.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('한글입력')
    mapping_VALORE = {'old': 'Indietro_articolo', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'tasto_Layout', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'commit_composizione', 'feed': 'feed_tasto', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'inviare', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Cronologia', 'pair': '한쌍', 'char': 'dati_di_tipo_carattere', 'VOWEL': '가운뎃소리목록', 'right': 'DESTRA', 'value': 'VALORE', 'text': 'testo'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
