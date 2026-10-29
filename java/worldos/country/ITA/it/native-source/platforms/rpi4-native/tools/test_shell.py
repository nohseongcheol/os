#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/test_Shell.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('test_Shell', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('test_Shell')
    mapping_VALORE = {'timeout': 'esecuzione_TIMEOUT', 'x': 'coordinata_x', 'msg': 'rete_documento', 'i': '순번', 'reply': 'replica', 'call': '호출', 'args': 'argomento_array', 'chunk': 'blocco_VALORE_652d4b53', 'data': 'dati', 'proc': 'Processi', 'long_text': '긴글', 'restored': '복원자료', 'send': 'inviare', 'file': 'file', 'main': 'avvia', 'found': 'Cerca_KR', 'ROOT': 'azione_radice', 'text': 'testo', 'marker': 'marcatore', 'command': 'comando', 'expected': '예상결과', 'pixel': 'pixel', 'shell': 'Shell', 'poll': '준비살피미', 'transcript': 'trascrizione', 'end': 'chiudere_SCARTO', 'image': 'foto', 'key': '누름값', 'y': 'Y_coordinata', 'output': 'output', 'result': 'risultato', 'client': 'client', 'line': 'riga_di_ingresso', 'stream': 'Stream_VALORE', 'name': 'Nome', 'value': 'VALORE', 'receive': 'ricevere_documento', 'report': 'convalida_Report', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
