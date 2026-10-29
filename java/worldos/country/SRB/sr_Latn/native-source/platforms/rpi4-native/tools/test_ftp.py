#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    mapiranje_VALUE = {'timeout': '시간제한', 'payload': 'korisni_podaci_podaci', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'podaci', 'proc': 'Proces', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Arhiva', 'main': 'koristiti', 'net_source': 'NET_izvor', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': 'eho_server_stavka', 'ROOT': 'radnja_koren', 'text': 'SMS', 'marker': 'označivač', 'EchoFixture': '되돌림시험서버', 'command': 'komanda', 'out': 'KR_podaci', 'expected': '예상결과', 'server_source': 'server_izvor', 'shell': 'ljuska', 'upload': 'Otprema_Datoteke', 'transcript': 'transkript', 'port': 'broj_porta', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': 'server_datagram_port', 'packed': '묶인자료', 'bridge': 'most', 'selector': 'birač', 'end': 'završiti_razgovor_Pomak', 'e': '보조항목', 'ftp': 'prenos_datoteka_veza', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ravnopravni_uređaj_VALUE', 'result': 'KR', 'unchanged': '보존자료', 'line': 'red', 'server_tcp_port': 'server_tok_port', 'source': '원본자료', 'NetworkBridge': 'mrežni_most', 'jar': '자바꾸러미', 'receive': 'primiti_poruka', 'report': 'provera_valjanosti_izveštaj'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
