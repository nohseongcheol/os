#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/test_FTP.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('test_FTP', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('test_FTP')
    toewijzing_WAARDE = {'timeout': 'uitvoerbewerking_TIMEOUT', 'payload': 'payload_gegevens', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'gegevens', 'proc': 'Proces', 'code': 'instructie_REEKS', 'linux': '리눅스파일', 'archive': 'Archief', 'main': 'starten', 'net_source': 'NET_bron', 'temporary': '임시자원', 'static_source': 'statisch_bron', 'java_source': '자바원문', 'echo': 'echo_server_invoer', 'ROOT': 'Taken_wortel', 'text': 'tekst', 'marker': 'markering', 'EchoFixture': '되돌림시험서버', 'command': 'opdracht', 'out': 'HR_gegevens', 'expected': '예상결과', 'server_source': 'server_bron', 'shell': 'Shell', 'upload': 'Upload_Files', 'transcript': 'transcriptie', 'port': 'poortnummer', 'native': 'systeemeigen', 'elf': 'uitvoerbaar_bestand', 'server_udp_port': 'server_datagram_poort', 'packed': '묶인자료', 'bridge': 'brug', 'selector': 'selector', 'end': 'beëindigen_VERSCHUIVING', 'e': '보조항목', 'ftp': 'bestandsoverdracht_verbinding', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'peer_WAARDE', 'result': 'resultaat', 'unchanged': '보존자료', 'line': 'invoerregel', 'server_tcp_port': 'server_Stream_poort', 'source': '원본자료', 'NetworkBridge': 'brug_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'ontvangen_e_mail', 'report': 'validatie_Rapport'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
