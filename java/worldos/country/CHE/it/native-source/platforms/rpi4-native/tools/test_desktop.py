#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/test_PC.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('test_PC', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('test_PC')
    mapping_VALORE = {'x': 'coordinata_x', 'typing': '글자입력', 'message': 'informativa_SMS', 'start': 'avvia', 'down': '누르는중', 'exact': 'IDENTICO_VALORE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'simbolo', 'j': '안쪽순번', 'deadline': 'scadenza_time', 'proc': 'Processi', 'data': 'dati', 'main': 'avvia', 'w': '너비값', 'init': '초기값', 'block': 'blocco_di_dati', 'ROOT': 'azione_radice', 'text': 'testo', 'marker': 'marcatore', 'report': 'convalida_Report', 'until': '까지', 'clipboard': 'Appunti_VALORE', 'dst': 'meta_e_mail', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'trascrizione', 'port': 'numero_di_porta', 'offset': 'SCARTO_VALORE', 'h': 'richiesto_altezza_VALORE', 'src': '원본주소', 'event': 'Evento', 'encoding': 'set_di_caratteri', 'size': 'Dimensione', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_coordinata', 'output': 'output', 'symbol': 'simbolo_VALORE', 'client': 'client', 'char': 'dati_di_tipo_carattere', 'rgb': '빛삼원색'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
