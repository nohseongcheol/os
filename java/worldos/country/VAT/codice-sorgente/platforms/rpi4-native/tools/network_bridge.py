#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/bridge_3de4fe3a.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('bridge_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('bridge_3de4fe3a')
    mapping_VALORE = {'response': 'risposta', 'parts': 'percorso_componente', 's': 'stringa_dati', 'i': '순번', 'close': 'Chiudi', 'forward': '전달규칙', 'slip_input': 'SLIP_input', 'self': '자신', 'item': 'voce_VALORE', 'flags': 'configurazione_BITS', 'ftp_port': 'trasferimento_di_file_numero_di_porta', 'args': 'argomento_array', 'server': 'server_VALORE', 'data': 'dati', 'ethernet_input': 'Ethernet_input', 'trace_packet': 'analisi_pacchetto', 'GATEWAY': 'gateway_hardware_e_mail', 'rule': 'riga_VALORE_c689d407', 'protocol': 'rete_ABI', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'host', 'ack': '확인번호', 'serial_port': 'porta_COM_numero', 'readers': '읽기대상들', 'guest': 'guest', 'destination': 'meta_dati_e_mail', 'ethernet_port': 'porta_Ethernet', 'b': 'SECONDO_VALORE', 'MAC': 'indirizzo_reale', 'arp': 'risoluzione_dell_indirizzo_pacchetto', 'writable': 'scrivibile', 'direction': 'direzione', 'seq': 'ordine_numero', 'frame': 'esecuzione_frame', 'loop': 'Cicli_VALORE', 'port': 'numero_di_porta', 'offset': 'SCARTO_VALORE', 'readable': '읽을수있음', 'c': 'punto_di_codice', 'p': 'dati_funzione', 'writers': '쓰기대상들', 'IP': 'indirizzo_Internet_VALORE', 'e': '보조항목', 'n': 'articolo_CONTA_NUMERI', 'packet': 'pacchetto_dati', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'bridge_3de4fe3a', 'window': 'Finestra', 'capture': 'acquisire'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
