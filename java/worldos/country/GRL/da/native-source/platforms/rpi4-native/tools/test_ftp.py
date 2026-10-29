#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/test_FTP.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('test_FTP', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('test_FTP')
    tilknytning_VÆRDI = {'timeout': 'udførelse_TIMEOUT', 'payload': 'nyttedata_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Proces', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Arkiv', 'main': 'Kør_2', 'net_source': 'NET_kilde', 'temporary': '임시자원', 'static_source': 'statisk_kilde', 'java_source': '자바원문', 'echo': 'ekko_server_post', 'ROOT': 'To_do_rod', 'text': 'Tekst', 'marker': 'mærke', 'EchoFixture': '되돌림시험서버', 'command': 'Kommando', 'out': 'KR_data', 'expected': '예상결과', 'server_source': 'server_kilde', 'shell': 'Shell', 'upload': 'Upload_Filer', 'transcript': 'afskrift', 'port': 'portnummer', 'native': 'oprindelig', 'elf': 'eksekverbar_fil', 'server_udp_port': 'server_datagram_port', 'packed': '묶인자료', 'bridge': 'bro', 'selector': 'selektor', 'end': 'afslutte_et_opkald_FORSKYDNING', 'e': '보조항목', 'ftp': 'filoverførsel_forbindelse', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'peer_VÆRDI', 'result': 'KR', 'unchanged': '보존자료', 'line': 'Linje', 'server_tcp_port': 'server_strøm_port', 'source': '원본자료', 'NetworkBridge': 'bro_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'modtage_mail', 'report': 'validering_rapport'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
