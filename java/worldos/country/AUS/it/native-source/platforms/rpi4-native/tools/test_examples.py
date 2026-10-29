#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/예제시험.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('예제시험')
    mapping_VALORE = {'count': 'voce_CONTA_NUMERI', 'exact': 'IDENTICO_VALORE', 'expected_file': '예상파일', 'ftp_port': 'trasferimento_di_file_numero_di_porta', 'data': 'dati', 'graphics_command': 'grafica_comando', 'main': 'avvia', 'row': 'riga_funzione', 'init': '초기값', 'target': 'target', 'ROOT': 'azione_radice', 'text': 'testo', 'binary': 'base_2', 'out': 'KR_dati', 'entry': 'punto_di_ingresso', 'got': 'RICEV_SCAD_CONTA_NUMERI', 'port': 'numero_di_porta', 'graphics_start': 'START_disegno', 'col': 'colonna_funzione', 'begin': 'START_SCARTO', 'kind': 'Valore_categoria', 'selector': 'selettore', 'n': 'articolo_CONTA_NUMERI', 'key': '누름값', 'y': 'Y_coordinata', 'client': 'client', 'line': 'riga_di_ingresso', 'report': 'convalida_Report', 'language': 'Lingua', 'x': 'coordinata_x', 'start': 'avvia', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'inviare_elenco', 'payload': 'payload_dati', 'proc': 'Processi', 'w': '너비값', 'temporary': '임시자원', 'echo': 'eco_schermo_server_voce', 'label': 'nome_tabella', 'content': 'Contenuto_VALORE', 'argument': '전달값', 'EchoServers': 'eco_schermo_Server', 'marker': 'marcatore', 'expected': '예상결과', 'test_language': 'test_Lingua', 'filename': 'File_voce_nome', 'shell': 'Shell', 'color': '색상', 'transcript': 'trascrizione', 'offset': 'SCARTO_VALORE', 'h': 'richiesto_altezza_VALORE', 'run': 'Esegui_comando', 'c': 'punto_di_codice', 'path': 'percorso', 'encoding': 'set_di_caratteri', 'end': 'chiudere_SCARTO', 'ftp': 'trasferimento_di_file_connessione', 'pixels': '화소들', 'symbol': 'simbolo_VALORE', 'source': '원본자료', 'name': 'Nome', 'receive': 'ricevere_documento', 'manifest': 'aggregare_manifesto'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
