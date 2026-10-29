#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/원격한글시험.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('원격한글시험')
    mapping_VALORE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'avvia', 'profile': 'Profilo', 'focused': 'Evidenziata', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALORE', 'log': 'LOG_riga', 'args': 'argomento_array', 'deadline': 'scadenza_time', 'data': 'dati', 'candidate': 'candidato', 'logs': '기록들', 'kw': 'argomento_predefinito', 'number': '수치', 'main': 'avvia', 'ready': '준비완료', 'found': 'Cerca_KR', 'guest': 'guest', 'ROOT': 'azione_radice', 'marker': 'marcatore', 'text': 'testo', 'out': 'KR_dati', 'env': 'ambiente', 'f': 'File_voce', 'port': 'numero_di_porta', 'offset': 'SCARTO_VALORE', 'version': 'numero_di_versione', 'p': 'dati_funzione', 'selector': 'selettore', 'xvfb': 'virtuale_display', 'display': 'display', 'n': 'articolo_CONTA_NUMERI', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtuale_input_strumento', 'name': 'Nome', 'window': 'Finestra', 'report': 'convalida_Report', 'work': '작업경로'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
