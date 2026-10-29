#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/test_Swing.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('test_Swing', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('test_Swing')
    mapping_VALORE = {'wait': '기다리기', 'x': 'coordinata_x', 's': 'stringa_dati', 'i': '순번', 'sel': 'selettore_a916db4e', 'seconds': '초단위', 'log': 'LOG_riga', 'data': 'dati', 'at': 'Regolari_funzione', 'send': 'inviare', 'main': 'avvia', 'req': 'richiesta_VALORE', 'hot': 'collegamento_VALORE', 'pump': 'handle_evento', 'ROOT': 'azione_radice', 'marker': 'marcatore', 'b': 'SECONDO_VALORE', 'command': 'comando', 'shell': 'Shell', 'f': 'File_voce', 'click': 'clic_pulsante', 'k': '셋째순번', 'c': 'punto_di_codice', 'r': '반환값', 'p': 'dati_funzione', 'command_mode': 'comando_MODA', 'end': 'chiudere_SCARTO', 'classes': 'Corso_percorso', 'key': '누름값', 'y': 'Y_coordinata', 'result': 'risultato', 'report': 'convalida_Report', 'dest': 'meta_VALORE_funzione', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
