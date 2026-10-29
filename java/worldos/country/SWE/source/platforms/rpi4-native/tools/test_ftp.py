#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/test_FTP.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('test_FTP', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('test_FTP')
    mappning_värde = {'timeout': 'körning_TIMEOUT', 'payload': 'nyttolast_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Process', 'code': 'instruktion_SEKVENS', 'linux': '리눅스파일', 'archive': 'Arkiv', 'main': 'Kör', 'net_source': 'NET_källa', 'temporary': '임시자원', 'static_source': 'statisk_källa', 'java_source': '자바원문', 'echo': 'UppdateraSkärm_server_post', 'ROOT': 'åtgärd_rot', 'text': 'text', 'marker': 'markör_8b722c5f', 'EchoFixture': '되돌림시험서버', 'command': 'kommando', 'out': 'KR_data', 'expected': '예상결과', 'server_source': 'server_källa', 'shell': 'Shell', 'upload': 'Upload_Filer', 'transcript': 'avskrift', 'port': 'portnummer', 'native': 'ursprunglig', 'elf': 'körbar_fil_fil', 'server_udp_port': 'server_datagram_port', 'packed': '묶인자료', 'bridge': 'brygga', 'selector': 'väljare', 'end': 'avsluta_FÖRSKJUTNING', 'e': '보조항목', 'ftp': 'filöverföring_kontakt', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'peer_värde', 'result': 'RESULTAT', 'unchanged': '보존자료', 'line': 'inmatningsrad', 'server_tcp_port': 'server_flöde_port', 'source': '원본자료', 'NetworkBridge': 'brygga_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'få_dokument', 'report': 'validering_Rapport'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
