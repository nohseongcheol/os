#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/test_FTP.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('test_FTP', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('test_FTP')
    tildeling_VERDI = {'timeout': 'kjøring_TIMEOUT', 'payload': 'nyttelast_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Prosess', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Arkiv', 'main': 'Kjør_2', 'net_source': 'netto_kilde', 'temporary': '임시자원', 'static_source': 'statisk_kilde', 'java_source': '자바원문', 'echo': 'oppdatere_skjerm_server_oppføring', 'ROOT': 'speile_rot', 'text': 'Tekst', 'marker': 'tusj', 'EchoFixture': '되돌림시험서버', 'command': 'Kommando', 'out': 'KR_data', 'expected': '예상결과', 'server_source': 'server_kilde', 'shell': 'Shell', 'upload': 'Upload_Filer', 'transcript': 'utskrift', 'port': 'portnummer', 'native': 'opprinnelig', 'elf': 'kjørbar_fil', 'server_udp_port': 'server_datagram_port', 'packed': '묶인자료', 'bridge': 'bro', 'selector': 'velger', 'end': 'avslutte_en_samtale_FORSKYVNING', 'e': '보조항목', 'ftp': 'filoverføring_kontakt', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'node_VERDI_6a3b6fa7', 'result': 'KR', 'unchanged': '보존자료', 'line': 'Linje', 'server_tcp_port': 'server_strøm_port', 'source': '원본자료', 'NetworkBridge': 'bro_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'motta_e_post', 'report': 'validering_rapport'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
