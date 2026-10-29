#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/test_protokol_FTP.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_protokol_FTP', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('test_protokol_FTP')
    대응 = {'timeout': 'spuštění_TIMEOUT', 'payload': 'vytížení_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Proces', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Archiv', 'main': 'Spustit_2', 'net_source': 'čistý_zdroj', 'temporary': '임시자원', 'static_source': 'statický_zdroj', 'java_source': '자바원문', 'echo': 'zobrazení_výsledků_server_položka', 'ROOT': 'akce_kořen', 'text': 'text', 'marker': 'značka', 'EchoFixture': 'zobrazení_výsledků_testovací_přípravek', 'command': 'příkaz', 'out': 'KV_data', 'expected': '예상결과', 'server_source': 'server_zdroj', 'shell': 'prostředí', 'upload': 'Upload_Files', 'transcript': 'přepis', 'port': 'číslo_portu', 'native': 'nativní', 'elf': 'spustitelný_soubor', 'server_udp_port': 'server_datagram_port', 'packed': '묶인자료', 'bridge': 'most', 'selector': 'selektor', 'end': 'konec_POSUN', 'e': '보조항목', 'ftp': 'přenos_souborů_kontakt', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'partner_HODNOTA', 'result': 'VÝSLEDEK', 'unchanged': '보존자료', 'line': 'vstupní_řádek', 'server_tcp_port': 'server_tok_port', 'source': '원본자료', 'NetworkBridge': 'most_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'dostat_e_mail', 'report': 'ověření_Zpráva'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
