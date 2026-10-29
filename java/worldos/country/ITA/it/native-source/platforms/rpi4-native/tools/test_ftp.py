#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/test_FTP.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('test_FTP', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('test_FTP')
    mapping_VALORE = {'timeout': 'esecuzione_TIMEOUT', 'payload': 'payload_dati', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': 'blocco_VALORE_652d4b53', 'data': 'dati', 'proc': 'Processi', 'code': 'istruzione_SEQUENZA', 'linux': '리눅스파일', 'archive': 'Archivio', 'main': 'avvia', 'net_source': 'NET_fonte', 'temporary': '임시자원', 'static_source': 'statico_fonte', 'java_source': '자바원문', 'echo': 'eco_schermo_server_voce', 'ROOT': 'azione_radice', 'text': 'testo', 'marker': 'marcatore', 'EchoFixture': 'eco_schermo_fixture', 'command': 'comando', 'out': 'KR_dati', 'expected': '예상결과', 'server_source': 'server_fonte', 'shell': 'Shell', 'upload': 'Upload_File', 'transcript': 'trascrizione', 'port': 'numero_di_porta', 'native': 'nativo_fd019377', 'elf': 'eseguibile', 'server_udp_port': 'server_datagramma_porta', 'packed': '묶인자료', 'bridge': 'bridge', 'selector': 'selettore', 'end': 'chiudere_SCARTO', 'e': '보조항목', 'ftp': 'trasferimento_di_file_connessione', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'peer_VALORE', 'result': 'risultato', 'unchanged': '보존자료', 'line': 'riga_di_ingresso', 'server_tcp_port': 'server_Stream_porta', 'source': '원본자료', 'NetworkBridge': 'bridge_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'ricevere_documento', 'report': 'convalida_Report'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
