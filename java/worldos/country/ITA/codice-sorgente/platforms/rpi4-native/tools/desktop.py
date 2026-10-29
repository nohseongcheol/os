#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/PC_Vista.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('PC_Vista', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('PC_Vista')
    mapping_VALORE = {'count': 'voce_CONTA_NUMERI', 'special': '특수글쇠', 'error': 'errore', 'exact': 'IDENTICO_VALORE', 'network': 'rete', 'closed': 'reparto_IT_chiusa', 'length': 'durata_VALORE', 'opened': '열림', 'ftp_port': 'trasferimento_di_file_numero_di_porta', 'server': 'server_VALORE', 'resources': 'Risorse', 'data': 'dati', 'shift': 'tasto_MAIUSC', 'send': 'inviare', 'run_desktop': 'eseguire_PC', 'protocol': 'rete_ABI', 'forwards': '전달규칙들', 'host': 'host', 'text': 'testo', 'korean': '한글여부', 'port': 'numero_di_porta', 'signum': 'segnale_numero', 'version': 'numero_di_versione', 'parser': 'parser', 'bridge': 'bridge', 'kind': 'Valore_categoria', 'tail': '끝부분', 'size': 'Dimensione', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_coordinata', 'prefix': 'interlinea_parte', 'client': 'client', 'char': 'dati_di_tipo_carattere', 'work': '작업경로', 'Keyboard': 'tastiera', 'x': 'coordinata_x', 'down': '누르는중', 'net': 'bridge_voce', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argomento_array', 'Hangul': '한글조합', 'chunk': 'blocco_VALORE_652d4b53', 'proc': 'Processi', 'Desktop': 'CONNETTI_PC', 'buttons': '단추들', 'thread': 'esecutoreAsincrono', 'pressed': '눌림', 'previous': 'Indietro', 'toggle': 'SWITCH_MODA', 'command': 'comando', 'sock': 'socket_VALORE', 'frame': 'esecuzione_frame', 'ctrl': 'CTRL', 'path': 'percorso', 'cp': 'codifica_dei_caratteri', 'terminate': 'terminare', 'security': 'Sicurezza', 'vnc_port': '원격화면접속번호', 'body': 'corpo_del_testo', 'index': 'CERCA_INDICE', 'exited': '종료됨', 'keysym': 'tasto_simbolo', 'output': 'output', 'keyboard': 'tastiera_voce', 'interrupted': '가로채기됨', 'listener': 'porta_di_ricezione', 'reader': 'Lettore', 'NetworkBridge': 'bridge_3de4fe3a', 'gui': 'disegno_schermata', 'worker': 'elaborazione_task'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
