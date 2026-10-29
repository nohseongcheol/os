#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/부팅시험.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('부팅시험')
    mapping_VALORE = {'timeout': 'esecuzione_TIMEOUT', 'response': 'risposta', 'msg': 'rete_documento', 'exact': 'IDENTICO_VALORE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Esegui', 'cancel': 'Chiudi_operazione', 'cmd_byte': 'comando_byte', 'reply': 'replica', 'points': '지점들', 'server': 'server_VALORE', 'data': 'dati', 'prompt': 'prompt', 'enter': 'immettere', 'imported': '들여온파일', 'send': 'inviare', 'main': 'avvia', 'ROOT': 'azione_radice', 'text': 'testo', 'first_gui': '첫화면', 'pixel': 'pixel', 'java_class': '자바클래스', 'upload': 'Upload_File', 'pixels_file': 'pixel_File', 'pixels_data': 'pixel_dati', 'edit': 'Modifica_VALORE', 'receive_until': '표시까지받기', 'selector': 'selettore', 'size': 'Dimensione', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECONDO_GUI', 'y': 'Y_coordinata', 'result': 'risultato', 'samples': '예제들', 'client': 'client', 'line': 'riga_di_ingresso', 'report': 'convalida_Report', 'work': '작업경로', 'x': 'coordinata_x', 'python_checks': '파이썬검사', 'download': 'download', 'greeting': 'messaggio_di_saluto_ae353e94', 'dims': '치수', 'chunk': 'blocco_VALORE_652d4b53', 'deadline': 'scadenza_time', 'proc': 'Processi', 'content': 'Contenuto_VALORE', 'block': 'blocco_di_dati', 'marker': 'marcatore', 'command': 'comando', 'expected': '예상결과', 'shell': 'Shell', 'drawing': 'disegno_percorso', 'f': 'File_voce', 'transcript': 'trascrizione', 'offset': 'SCARTO_VALORE', 'path': 'percorso', 'screenshot': 'screenshot', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': 'schermata_client', 'output': 'output', 'stream': 'Stream_VALORE', 'cmd': '명령인수', 'name': 'Nome', 'qmp': '모의제어접속'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
