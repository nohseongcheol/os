#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/Esegui_File.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('Esegui_File', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('Esegui_File')
    mapping_VALORE = {'timeout': 'esecuzione_TIMEOUT', 's': 'stringa_dati', 'i': '순번', 'match': '일치', 'files': 'elenco_file', 'program': 'app', 'executable': 'eseguibile_foto', 'args': 'argomento_array', 'chunk': 'blocco_VALORE_652d4b53', 'data': 'dati', 'proc': 'Processi', 'send': 'inviare', 'main': 'avvia', 'marker': 'marcatore', 'command': 'comando', 'include': 'includere', 'dumped': '갈무리자료', 'run': 'Esegui_comando', 'p': 'dati_funzione', 'parser': 'parser', 'options': 'Opzioni', 'kind': 'Valore_categoria', 'selector': 'selettore', 'upload_data': 'Upload_dati', 'end': 'chiudere_SCARTO', 'n': 'articolo_CONTA_NUMERI', 'd': 'meta_dati', 'key': '누름값', 'output': 'output', 'line': 'riga_di_ingresso', 'name': 'Nome', 'upload_name': 'Upload_nome', 'receive': 'ricevere_documento'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
